#!/usr/bin/env python3
import sys
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from lxml import etree

def parse_xml_to_model(root, store, parent=None):
    """✅ Парсит XML в TreeStore (игнорирует комментарии и namespace)"""
    for elem in root:
        # Пропускаем комментарии
        if isinstance(elem, etree._Comment):
            continue

        # Пропускаем namespace элементы
        if not isinstance(elem.tag, str) or elem.tag.startswith('{'):
            continue

        text = (elem.text or '').strip() if elem.text else ''
        attrib = str(dict(elem.attrib)) if elem.attrib else ''
        value = text or attrib or ''

        tree_iter = store.append(parent, [elem.tag, value, elem.tag])
        parse_xml_to_model(elem, store, tree_iter)

def model_to_xml(store, parent_iter, xml_parent):
    """Рекурсивно строит XML из модели TreeStore"""
    if parent_iter is None:
        return

    # Get the first child if exists
    child_iter = store.iter_children(parent_iter)

    while child_iter:
        tag = store[child_iter][0]
        text = store[child_iter][1]

        # Create XML element
        elem = etree.SubElement(xml_parent, tag)
        if text:
            elem.text = text.strip()

        # Process grandchildren
        model_to_xml(store, child_iter, elem)

        # Move to next sibling
        child_iter = store.iter_next(child_iter)

def on_text_edited(renderer, path_str, new_text, store):
    """Обработчик редактирования ячейки"""
    try:
        path = Gtk.TreePath.new_from_string(path_str)
        tree_iter = store.get_iter(path)
        if tree_iter:
            store[tree_iter][1] = new_text
            print(f"✓ Updated row {path_str}: '{new_text}'")
    except Exception as e:
        print(f"Error editing cell: {e}")

class XmlEditorWindow(Gtk.Window):
    def __init__(self, filename):
        # ✅ Извлекаем только имя файла для заголовка
        file_basename = os.path.basename(filename)
        # ✅ Добавляем имя файла в заголовок окна
        window_title = f"XML Tree Editor - {file_basename}"
        super().__init__(title=window_title)

        self.filename = filename
        self.original_root_tag = None
        self.root_element = None  # Store the root element for saving

        self.set_default_size(900, 700)
        self.connect("destroy", Gtk.main_quit)

        # Чтение и парсинг XML
        try:
            parser = etree.XMLParser(recover=True, remove_comments=True)
            tree = etree.parse(filename, parser)
            root = tree.getroot()
            self.original_root_tag = root.tag
            self.root_element = root
            print(f"Loaded XML root: <{self.original_root_tag}>")
        except Exception as e:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                     Gtk.ButtonsType.OK, f"Ошибка чтения XML: {str(e)}")
            dialog.run(); dialog.destroy(); sys.exit(1)

        # Модель TreeStore: [tag, value/text, display_tag]
        self.store = Gtk.TreeStore(str, str, str)
        parse_xml_to_model(root, self.store)

        # ✅ ФИКС: правильно считаем количество корневых элементов
        root_count = self.store.iter_n_children(None)
        print(f"Parsed {root_count} root elements")

        # TreeView с expanders
        treeview = Gtk.TreeView(model=self.store)
        treeview.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        treeview.set_show_expanders(True)
        treeview.expand_all()

        # Колонка Tag с КРАСНЫМ цветом текста
        renderer_tag = Gtk.CellRendererText()

        # ✅ Устанавливаем красный цвет текста
        renderer_tag.set_property('foreground', 'red')

        # Если нужно сделать текст жирным тоже, можно добавить:
        # renderer_tag.set_property('weight', 700)  # bold

        column_tag = Gtk.TreeViewColumn("Tag", renderer_tag, text=2)
        column_tag.set_expand(True)
        treeview.append_column(column_tag)

        # Колонка Value (редактируемая)
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property('editable', True)
        # ✅ FIX: Pass store as user_data to callback
        renderer_text.connect('edited', on_text_edited, self.store)
        column_text = Gtk.TreeViewColumn("Value (text/attributes)", renderer_text, text=1)
        column_text.set_expand(True)
        treeview.append_column(column_text)

        scrolled = Gtk.ScrolledWindow()
        scrolled.add(treeview)

        # Toolbar с кнопками expand/collapse
        toolbar = Gtk.Toolbar()
        toolbar.set_style(Gtk.ToolbarStyle.ICONS)

        btn_expand_all = Gtk.ToolButton()
        btn_expand_all.set_icon_name("go-down")
        btn_expand_all.connect('clicked', lambda x: treeview.expand_all())
        toolbar.insert(btn_expand_all, -1)

        btn_collapse_all = Gtk.ToolButton()
        btn_collapse_all.set_icon_name("go-up")
        btn_collapse_all.connect('clicked', lambda x: treeview.collapse_all())
        toolbar.insert(btn_collapse_all, -1)

        # Панель кнопок
        hbox = Gtk.Box(spacing=6)
        btn_save = Gtk.Button(label="💾 Save")
        btn_save.connect('clicked', self.on_save)
        btn_close = Gtk.Button(label="❌ Close")
        btn_close.connect('clicked', Gtk.main_quit)
        hbox.pack_start(btn_save, False, False, 0)
        hbox.pack_start(btn_close, False, False, 0)

        # Layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.pack_start(toolbar, False, False, 0)
        vbox.pack_start(scrolled, True, True, 0)
        vbox.pack_start(hbox, False, False, 0)
        self.add(vbox)
        self.show_all()

        self.treeview = treeview

    def on_save(self, button):
        """Сохранение с правильной структурой"""
        try:
            if self.original_root_tag:
                # Create new root element
                root = etree.Element(self.original_root_tag)

                # Start from the first child of the root in TreeStore
                root_iter = self.store.get_iter_first()
                if root_iter:
                    # Get children of root (which correspond to XML children)
                    child_iter = self.store.iter_children(root_iter)
                    model_to_xml(self.store, root_iter, root)

                # Create and save the XML tree
                tree = etree.ElementTree(root)
                tree.write(self.filename, pretty_print=True,
                          xml_declaration=True, encoding='utf-8')

                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                         Gtk.ButtonsType.OK,
                                         f"✅ Сохранено: {self.filename}")
            else:
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                                         Gtk.ButtonsType.OK, "Модель пуста!")
            dialog.run(); dialog.destroy()
        except Exception as e:
            import traceback
            traceback.print_exc()
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                     Gtk.ButtonsType.OK, f"Ошибка сохранения: {str(e)}")
            dialog.run(); dialog.destroy()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 dialog_xml_tree_editor.py <xml_file>")
        sys.exit(1)

    filename = sys.argv[1]
    print(f"Opening: {filename}")
    win = XmlEditorWindow(filename)
    Gtk.main()
