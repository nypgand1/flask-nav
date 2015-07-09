from flask import current_app

from dominate import tags
from visitor import Visitor


class BaseRenderer(Visitor):
    def visit_object(self, node):
        if current_app.debug:
            return tags.comment(
                'no implementation in {} to render {}'.format(
                    self.__class__.__name__, node.__class__.__name__,
                ))
        return ''


class SimpleRenderer(BaseRenderer):
    def visit_Link(self, node):
        return tags.a(node.title, **node.attribs)

    def visit_Navbar(self, node):
        cont = tags.nav(_class='navbar', id=node.id)
        ul = cont.add(tags.ul())

        for item in node.items:
            ul.add(tags.li(self.visit(item)))

        return cont

    def visit_View(self, node):
        kwargs = {}
        if node.active:
            kwargs['_class'] = 'active'
        return tags.a(node.title,
                      href=node.get_url(),
                      title=node.title,
                      **kwargs)

    def visit_Subgroup(self, node):
        group = tags.ul(_class='subgroup')
        title = tags.span(node.title)

        if node.active:
            title.attributes['class'] = 'active'

        for item in node.items:
            group.add(tags.li(self.visit(item)))

        return tags.div(title, group)

    def visit_Separator(self, node):
        return tags.hr(_class='separator')

    def visit_Label(self, node):
        return tags.span(node.title, _class='nav-label')
