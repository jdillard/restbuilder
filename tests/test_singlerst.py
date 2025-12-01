from os.path import join, exists
import io

from tests.utils import build_singlerst


def test_singlerst_combines_documents(src_dir, output_dir):
    """Test that singlerst builder combines multiple documents into one file."""
    test_src = join(src_dir, 'sphinx-directives/toctree')
    test_output = join(output_dir, 'singlerst/toctree')

    build_singlerst(test_src, test_output)

    # Should produce a single index.rst file
    output_file = join(test_output, 'index.rst')
    assert exists(output_file), "singlerst should create index.rst"

    # Read the output and verify it contains content from all documents
    with io.open(output_file, encoding='utf-8') as f:
        content = f.read()

    # Check that content from doc1 and doc2 is included
    assert 'Doc 1' in content, "Output should contain Doc 1 heading"
    assert 'This is document 1' in content, "Output should contain doc1 content"
    assert 'Doc 2' in content, "Output should contain Doc 2 heading"
    assert 'This is document 2' in content, "Output should contain doc2 content"

    # Check that document boundary anchors are generated
    assert '.. _document-doc1:' in content, "Output should have doc1 anchor"
    assert '.. _document-doc2:' in content, "Output should have doc2 anchor"


def test_singlerst_single_file_only(src_dir, output_dir):
    """Test that singlerst builder produces only one RST file."""
    test_src = join(src_dir, 'sphinx-directives/toctree')
    test_output = join(output_dir, 'singlerst/toctree-single')

    build_singlerst(test_src, test_output)

    # Should NOT produce separate doc1.rst and doc2.rst files
    assert not exists(join(test_output, 'doc1.rst')), "singlerst should not create doc1.rst"
    assert not exists(join(test_output, 'doc2.rst')), "singlerst should not create doc2.rst"

    # Should only have index.rst
    assert exists(join(test_output, 'index.rst')), "singlerst should create index.rst"
