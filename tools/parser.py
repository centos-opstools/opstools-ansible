# This class is responsible for transforming a file containing a mix
# of code and documentation into a set of `(code, documentation)`
# pairs.


class HashCommentParser(object):
    def __init__(self, fd):
        self.fd = fd

    # This class is an iterator, which means that after you do this:
    #
    #     with open('somefile') as fd:
    #         doc = HashCommentParser(fd)
    #
    # You can then iterate over `(code, documentation)` chunks
    # like this:
    #
    #         for codepart, docpart in doc:
    #             ...
    def __iter__(self):
        return self.iter_chunks()

    def iter_chunks(self):
        doc = []
        code = []
        indoc = False

        # Iterate over lines in the input file looking for
        # documentation (lines that start with `# `, preceded
        # by an arbitrary amount of whitespace).
        for line in self.fd:
            stripped = line.lstrip()

            # Rules for when we are already reading
            # a block of documentation.
            if indoc:
                if stripped.startswith('# '):
                    doc.append(stripped[2:])
                    continue
                elif stripped == '#\n':
                    doc.append('\n')
                    continue
                else:
                    indoc = False

            # Rules for when we think we are reading code.
            if not indoc:
                if stripped.startswith('# '):
                    # It looks like we're starting a new documentation
                    # chunk! If we have either an existing code or doc
                    # chunk, we should yield a pair back to the caller
                    # before starting to accumulate the new
                    # documentation.
                    if code or doc:
                        yield (code, doc)
                        code = []
                        doc = []

                    indoc = True
                    doc.append(stripped[2:])
                elif not stripped and not code:
                    continue
                else:
                    code.append(line)

        # Yield remaining blocks back to caller.
        yield (code, doc)
