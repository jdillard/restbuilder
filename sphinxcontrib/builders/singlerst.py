# -*- coding: utf-8 -*-
"""
    sphinxcontrib.builders.singlerst
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Single ReST file Sphinx builder.

    :copyright: Copyright 2012-2021 by Freek Dijkstra and contributors.
    :license: BSD, see LICENSE.txt for details.
"""

from __future__ import (print_function, unicode_literals, absolute_import)

from sphinx.util.nodes import inline_all_toctrees

from .rst import RstBuilder
from ..writers.rst import RstWriter


class SingleRstBuilder(RstBuilder):
    """
    A builder that combines all documents into a single RST file.
    """
    name = 'singlerst'

    def get_outdated_docs(self):
        """
        Return an iterable of input files that are outdated.
        """
        # Since all documents are combined into one, we always rebuild.
        return 'all documents'

    def get_target_uri(self, docname, typ=None):
        if docname == self.config.root_doc:
            return ''
        return '#document-' + docname

    def assemble_doctree(self):
        """Assemble all documents into a single doctree."""
        root_doc = self.config.root_doc
        tree = self.env.get_doctree(root_doc)
        # Inline all toctrees to merge all documents into the root doctree.
        tree = inline_all_toctrees(
            self, set(), root_doc, tree, colorfunc=lambda x: x, traversed=[]
        )
        tree['docname'] = root_doc
        # Resolve all references now that all documents are combined.
        self.env.resolve_references(tree, root_doc, self)
        return tree

    def prepare_writing(self, docnames):
        self.writer = RstWriter(self)

    def write(self, build_docnames, updated_docnames, method='update'):
        # This method overrides the base builder's write() to combine
        # all documents into a single file instead of writing each separately.
        docnames = self.env.all_docs
        self.prepare_writing(docnames)
        doctree = self.assemble_doctree()
        self.write_doc(self.config.root_doc, doctree)

    def finish(self):
        pass
