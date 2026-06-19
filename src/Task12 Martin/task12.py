# Task 12: Use case from stakeholder interview

import os
import re


# ------------------------------------------------------------
# CHANGE FILES HERE
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOURCE_FILE = os.path.join(
    BASE_DIR,
    "IndividualWindowDPP.ttl"
)

ALIGNMENT_FILE = os.path.join(
    BASE_DIR,
    "DPPO-CEON-simplified.ttl"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "task12_transformed_use_case.ttl"
)

REPORT_FILE = os.path.join(
    BASE_DIR,
    "task12_replacement_report.txt"
)

# Direction of the mapping
# source_to_target = left side becomes right side
# target_to_source = right side becomes left side
ALIGNMENT_DIRECTION = "source_to_target"


class Task12UseCaseTransformer:
    """
    Demonstrates Task 12 using use case data.

    This script:
    - Reads a use case file in TTL format
    - Reads an alignment file in TTL format
    - Finds CEON/DPPO terms that can be replaced
    - Saves a transformed TTL file
    - Saves a small report with the replacements
    """

    def load_file(self, file_path):
        """
        Loads a text file.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: File content.
        """

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def read_prefixes(self, text):
        """
        Reads prefixes from a TTL file.

        Args:
            text (str): TTL text.

        Returns:
            dict: Prefixes found in the file.
        """

        prefixes = {}

        pattern = r"@prefix\s+([A-Za-z0-9_-]+):\s+<([^>]+)>"

        for match in re.finditer(pattern, text):
            prefix = match.group(1)
            uri = match.group(2)
            prefixes[prefix] = uri

        return prefixes

    def short_term(self, uri, prefixes):
        """
        Turns a full URI into a short term if possible.

        Args:
            uri (str): Full URI.
            prefixes (dict): Prefix dictionary.

        Returns:
            str: Short term or full URI.
        """

        for prefix, base_uri in prefixes.items():
            if uri.startswith(base_uri):
                return prefix + ":" + uri.replace(base_uri, "")

        return "<" + uri + ">"

    def read_alignment(self, alignment_text):
        """
        Reads simple mappings from the alignment file.

        Args:
            alignment_text (str): Alignment TTL text.

        Returns:
            list: List of mappings.
        """

        mappings = []

        # Finds mappings written with full URI brackets
        pattern = r"<([^>]+)>\s+([A-Za-z0-9_:.-]+)\s+<([^>]+)>"

        for match in re.finditer(pattern, alignment_text):
            source = match.group(1)
            relation = match.group(2)
            target = match.group(3)

            if self.is_mapping_relation(relation):
                mappings.append(
                    {
                        "source": source,
                        "target": target,
                        "relation": relation
                    }
                )

        return mappings

    def is_mapping_relation(self, relation):
        """
        Checks if the relation is a mapping relation.

        Args:
            relation (str): Relation from the alignment file.

        Returns:
            bool: True if it is a mapping relation.
        """

        mapping_words = [
            "exactMatch",
            "closeMatch",
            "broadMatch",
            "narrowMatch",
            "equivalentClass",
            "equivalentProperty",
            "subClassOf",
            "subPropertyOf"
        ]

        for word in mapping_words:
            if word in relation:
                return True

        return False

    def make_replacement_map(self, mappings):
        """
        Creates a dictionary for replacements.

        Args:
            mappings (list): Mappings from the alignment file.

        Returns:
            dict: Replacement dictionary.
        """

        replacement_map = {}

        for mapping in mappings:

            if ALIGNMENT_DIRECTION == "source_to_target":
                old_value = mapping["source"]
                new_value = mapping["target"]
            else:
                old_value = mapping["target"]
                new_value = mapping["source"]

            replacement_map[old_value] = new_value

        return replacement_map

    def transform_text(self, source_text, replacement_map, prefixes):
        """
        Replaces terms in the use case text.

        Args:
            source_text (str): Original use case text.
            replacement_map (dict): Terms to replace.
            prefixes (dict): Prefixes from the source file.

        Returns:
            tuple: Transformed text and replacement report.
        """

        transformed_text = source_text
        report = []

        for old_uri, new_uri in replacement_map.items():

            old_short = self.short_term(old_uri, prefixes)
            new_short = self.short_term(new_uri, prefixes)

            uri_count = transformed_text.count("<" + old_uri + ">")
            short_count = transformed_text.count(old_short)

            total_count = uri_count + short_count

            if total_count > 0:
                transformed_text = transformed_text.replace(
                    "<" + old_uri + ">",
                    "<" + new_uri + ">"
                )

                transformed_text = transformed_text.replace(
                    old_short,
                    new_short
                )

                report.append(
                    f"{old_short} -> {new_short}   replacements: {total_count}"
                )

        return transformed_text, report

    def save_file(self, file_path, content):
        """
        Saves text to a file.

        Args:
            file_path (str): Output file path.
            content (str): Text to save.
        """

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def run(self):
        """
        Runs the Task 12 use case transformation.
        """

        print("Task 12 use case transformation")
        print("--------------------------------")

        print("\nSource file:")
        print(SOURCE_FILE)
        print("Exists:", os.path.exists(SOURCE_FILE))

        print("\nAlignment file:")
        print(ALIGNMENT_FILE)
        print("Exists:", os.path.exists(ALIGNMENT_FILE))

        if not os.path.exists(SOURCE_FILE):
            print("\nERROR: Source file was not found.")
            return

        if not os.path.exists(ALIGNMENT_FILE):
            print("\nERROR: Alignment file was not found.")
            return

        source_text = self.load_file(SOURCE_FILE)
        alignment_text = self.load_file(ALIGNMENT_FILE)

        prefixes = self.read_prefixes(source_text)
        mappings = self.read_alignment(alignment_text)
        replacement_map = self.make_replacement_map(mappings)

        print("\nMappings found:")
        print(len(mappings))

        transformed_text, report = self.transform_text(
            source_text,
            replacement_map,
            prefixes
        )

        self.save_file(OUTPUT_FILE, transformed_text)

        report_text = "Task 12 replacement report\n"
        report_text += "--------------------------\n\n"

        if len(report) == 0:
            report_text += "No replacements were found.\n"
            report_text += "This usually means that the alignment file and the use case file use different URI names.\n"
        else:
            report_text += "Replacements made:\n\n"

            for line in report:
                report_text += line + "\n"

        self.save_file(REPORT_FILE, report_text)

        print("\nReplacements made:")
        print(len(report))

        for line in report:
            print(line)

        print("\nOutput file:")
        print(OUTPUT_FILE)

        print("\nReport file:")
        print(REPORT_FILE)


if __name__ == "__main__":
    transformer = Task12UseCaseTransformer()
    transformer.run()