import bibtexparser

class References:

    def __init__(self, references_filename="webapp/static/references.bib"):
        with open(references_filename, "r") as references_bib_file:
            bibtex_str = references_bib_file.read()

        references_db = bibtexparser.loads(bibtex_str)

        self.references_str = {}

        for entry in references_db.entries:
            authors = entry.get("author", "").replace(" and", ", ").replace("\n", "")
            title = entry.get("title", "")
            year = entry.get("year", "")
            pages = entry.get("pages", "").replace("--", "-")
            book_title = entry.get("booktitle", "").replace("\n", "")
            doi = entry.get("url", "")
            article_journal = entry.get("journal", "")
            volume = entry.get("volume", "")
            number = entry.get("number", "")
            how_published = entry.get("howpublished", "")
            note = entry.get("note", "")

            if entry['ENTRYTYPE'] == "inproceedings":
                self.references_str[entry['ID']] = \
                    f"{authors}. {title}. In: {book_title}, pp. {pages} ({year}). [{doi}]({doi})"
            elif entry['ENTRYTYPE'] == "article":
                self.references_str[entry['ID']] = f"{authors}. {title}. {article_journal}, vol. {volume}, no. {number}, pp. {pages} ({year}). [{doi}]({doi})"
            elif entry['ENTRYTYPE'] == "misc":
                self.references_str[entry['ID']] = f"{authors}. {title} ({year}). {note}. [{how_published}]({how_published})"

        # citations
        self.citations_nr: dict[str, None | int] = {bib_id: None for bib_id in self.references_str.keys()}
        self.max_cite_nr = 1

        # referencing to citations
        # figures are in the order they are referenced
        self.figures_nr: dict[str, None | int] = {}
        self.max_figure_nr = 1

    def cite(self, *bib_ids) -> str:
        ref_numbers = []
        for bib_id in bib_ids:
            if self.citations_nr[bib_id] is None:
                self.citations_nr[bib_id] = self.max_cite_nr
                self.max_cite_nr += 1
            ref_numbers.append(self.citations_nr[bib_id])

        ref_numbers.sort()

        return f"[{", ".join(list(map(str, ref_numbers)))}]"

    def ref_figure(self, label: str) -> int:
        if label not in self.figures_nr:
            self.figures_nr[label] = self.max_figure_nr
            self.max_figure_nr += 1

        return self.figures_nr[label]

    def make_references_section(self) -> str:
        ref_section = "## References"
        ref_items = [(bib_id, ref_nr) for bib_id, ref_nr in self.citations_nr.items() if ref_nr is not None]
        ref_items.sort(key=lambda item: item[1])
        for bib_id, ref_nr in ref_items:
            ref_section += "\n\n[{}] {}".format(ref_nr, self.references_str[bib_id])

        return ref_section

if __name__ == "__main__":
    ref = References("../static/references.bib")