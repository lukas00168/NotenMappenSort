import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from PyPDF2 import PdfMerger
from tqdm import tqdm

SHEET_FOLDER_PATH = Path("/home/lukas/Dokumente/Noten/temp/OneDrive_2025-12-02/OneDrive_2025-12-04/Nach Stücken sortiert")
OUTPUT_PATH = Path("/home/lukas/Dokumente/Noten/temp/Notenmappen-Sortiert")

REPERTOIRE = [
    "Angels",
    # "Astronauten-Marsch",
    "Auf_der_Vogelwiese",
    "Bis_bald_auf_Wiederseh'n",
    "Blas'_Musik_in_die_Welt!",
    "Böhmische_Liebe",
    "Böhmischer_Traum",
    "Borsicka-Polka",
    "Bozner_Bergsteiger-Marsch",
    "Da_Capo",
    "Dem_Land_Tirol_die_Treue",
    "Die_Fischerin_vom_Bodensee",
    "Die_Sonne_geht_auf",
    "Ein_halbes_Jahrhundert",
    "Ein_Leben_Lang",
    "Ein_neuer_Tag",
    "Ein_Prosit",
    "Eine_letzte_Runde",
    "Euphoria",
    "Fuchsgraben",
    "Für_Helena",
    # "Griechischer_Wein",
    "Hoch_Badnerland",
    "Im_Eilschritt_nach_Sankt_Peter",
    "Im_Wäldchen",
    "In_der_Weinschenke",
    # "Jahresringe",
    "Kannst_du_Knödel_kochen",
    "Katharinen-Polka",
    "Kuschel-Polka",
    "Laubener_Schnellpolka",
    "Löffel-Polka",
    #"Morgenblüten",
    "Partyplanet",
    "Perger_Polka",
    "Pfeffer_und_Salz",
    "Polka_mit_Herz",
    "Rauschende_Birken",
    "Rosamunde",
    "Roy-Bianco",
    "Schunkelparade_Nr.2",
    "Stelldichein_in_Oberkrain",
    "Südböhmische_Polka",
    "Unsere_Reise_Woodstock",
    #"Viva_la_Vida_Woodstock",
    "Von_Freund_zu_Freund_Woodstock",
    "Wackelkontakt",
    "Wenn_der_Wein_blüht",
    "Wir_Musikanten",
    "Zwei_Herzen_Wachen_auf",
]

# define which folder contains which parts
FOLDER_TO_PART = {
    "Flöte 1 + Piccolo": ["Flöte_1_C", "Flöte_C", "Piccolo_C"],  # 1 mal
    "Flöte 1": ["Flöte_1_C", "Flöte_C"],  # 1 mal
    "Flöte 2": ["Flöte_2_C", "Flöte_C"],  # 2 mal
    "Klarinette 1": ["Klarinette_1_B"],  # 1 mal
    "Klarinette 2": ["Klarinette_23_B", "Klarinette_2_B"],  # 1 mal
    "Klarinette 3": ["Klarinette_23_B", "Klarinette_3_B"],  # 1 mal
    "Klarinette Es": [
        "Klarinette_Es",
        "Klarinette_2_Es",
        "Klarinette_E",
        "Klarinette_2_E",
    ],  # 1 mal
    "Alt-Saxophon 1": [
        "Alt-Saxophon_1_Es",
        "Alt-Saxophon_Es",
        "Alt-Saxophon_1_E",
        "Alt-Saxophon_E",
    ],  # 1 mal
    "Alt-Saxophon 2": [
        "Alt-Saxophon_2_Es",
        "Alt-Saxophon_Es",
        "Alt-Saxophon_2_E",
        "Alt-Saxophon_E",
    ],  # 1 mal
    "Tenor-Saxophon + BariSax": [
        "Tenor-Saxophon_1_B",
        "Tenor-Saxophon_12_B",
        "Tenor-Saxophon_2_B",
        "Tenor-Saxophon_B",
        "Bariton-Saxophon_Es",
        "Bariton-Saxophon_E",
    ],  # 1 mal
    "Trompete 1": ["Trompete_1_B", "Trompete_B", "Trompete_Solo_B"],  # 1 mal
    "Trompete 2": ["Trompete_2_B", "Tompete_2_B"],  # 1 mal
    "Trompete 3 + 4": ["Trompete_3_B", "Trompete_4_B"],  # 1 mal
    "Flügelhorn 1": ["Flügelhorn_1-B", "Flügelhorn_1_B"],  # 2 mal
    "Flügelhorn 2": ["Flügelhorn_2_B", "Flügelhorn_3_B"],  # 2 mal
    "Tenorhorn 1 in B": ["Tenorhorn_1-B", "Tenorhorn_1_B", "Tenorhorn_B"],  # 2 mal
    "Tenorhorn 2 in B": ["Tenorhorn_2_B", "Tenorhorn_B"],  # 1 mal
    "Horn 1 + 3 in F": [
        "Horn_1_F",
        "Horn_Melodie_1_F",
        "Horn_Melodie_F",
        "Horn_3_F",
    ],  # 1 mal
    "Horn 2 + 4 in F": [
        "Horn_2-F",
        "Horn_2_F",
        "Horn_Melodie_2_F",
        "Horn_Melodie_F",
        "Horn_4_F",
    ],  # 1 mal
    "Posaune 1": [
        "Posaune_1_C",
        "Posaune_1_C_Bass",
        "Posaune_Begleitung_1_C",
        "Posaune_C",
        "Posaune_Melodie_C",
    ],  # 1 mal
    "Posaune 2": [
        "Posaune_2_C",
        "Posaune_2_C_Bass",
        "Posaune_Begleitung_2_C",
        "Posaune_C",
        "Posaune_Melodie_C",
    ],  # 1 mal
    "Posaune 3": [
        "Posaune_3_C",
        "Posaune_3_C_Bass",
        "Posaune_Begleitung_3_C",
    ],  # 1 mal
    "Bariton in B": ["Bariton_B", "Bariton_1_B", "Bariton_B_Violin"],  # 2 mal
    "Bariton in C": ["Bariton_C", "Bariton_1_C"],  # 2 mal
    "Bass 1 in C": ["Bass_1_C", "Bass_C"],  # 1 mal
    "Bass 2 in C": ["Bass_2_C", "Bass_C"],  # 1 mal
    "Bass in B + Eb": [
        "Bass_1_B",
        "Bass_B",
        "Bass_B_Violin",
        "Bass_1_Es",
        "Bass_Es",
        "Bass_1_E",
        "Bass_E",
        "Bass_Es_Violin",
        "Bass_2_B",
    ],  # 1 mal
    "Partitur": ["Direktion", "Direktion_Di", "Partitur"],  # 1 mal
    "Schlagzeug": [
        "Schlagzeug",
        "Becken",
        "GroßeTrommel",
        "GroßeTrommel_Becken",
        "KleineTrommel",
        "Löffel_Solo",
        "Tamburin",
    ],
}

# Define replacements for missing parts
REPLACEMENTS = {
    "Alt-Saxophon 1": ["Klarinette Es"],
    "Alt-Saxophon 2": ["Alt-Saxophon 1", "Klarinette Es"],
    "Tenor-Saxophon + BariSax": ["Tenorhorn 1 in B"],
    "Bass 2 in C": ["Bass 1 in C"],
    "Flöte 2": ["Flöte 1"],
    "Horn 2 + 4 in F": ["Horn 1 + 3 in F"],
    "Klarinette 2": ["Klarinette 1"],
    "Klarinette 3": ["Klarinette 2", "Klarinette 1"],
    "Posaune 3": ["Posaune 2", "Posaune 1"],
    "Tenorhorn 2 in B": ["Tenorhorn 1 in B"],
    "Trompete 2": ["Trompete 1"],
    "Trompete 3 + 4": ["Trompete 2", "Trompete 1"],
    "Flügelhorn 2": ["Flügelhorn 1", "Trompete 2"],
    "Flügelhorn 1": ["Trompete 1"],
    "Bariton in B": ["Tenorhorn 2 in B", "Tenorhorn 1 in B"],
    "Bariton in C": ["Posaune 2", "Posaune 1"],
    "Bass 1 in C": ["Bass 2 in C"],
}

# make reverse dict for later sorting
_part_to_folder = defaultdict(list)
for _folder, _parts in FOLDER_TO_PART.items():
    for _part in _parts:
        _part_to_folder[_part].append(_folder)
PART_TO_FOLDER: Dict[str, List[str]] = dict(_part_to_folder)


def sort_folders(folders: Dict[str, set[Path]]) -> Dict[str, List[Path]]:
    return {
        folder: sorted(list(pdf_paths), key=lambda x: x.parts[-2])
        for folder, pdf_paths in folders.items()
    }


def merge_pdfs(pdf_paths: List[Path], output_path: Path):
    merger = PdfMerger()
    for pdf_path in pdf_paths:
        merger.append(str(pdf_path))
    merger.write(str(output_path))
    merger.close()


def create_folder_pdfs(folders: Dict[str, List[Path]]):
    # create OUTPUT_PATH if it does not exist
    if not OUTPUT_PATH.exists():
        OUTPUT_PATH.mkdir()

    for folder, pdf_paths in tqdm(folders.items(), desc="Erstellen der Mappen-PDFs:"):
        output_file = OUTPUT_PATH / (folder + ".pdf")
        merge_pdfs(pdf_paths, output_file)


def create_folders() -> Dict[str, set[Path]]:
    folders: Dict[str, set[Path]] = defaultdict(set)  # maps folder title to pdf path

    for song in REPERTOIRE:
        suffix = "_" + song + ".pdf"
        for part in os.listdir(SHEET_FOLDER_PATH / song):
            pdf_path = SHEET_FOLDER_PATH / song / part
            part = part[: -len(suffix)]
            destination_folders = PART_TO_FOLDER[part] if part in PART_TO_FOLDER else []
            for folder in destination_folders:
                folders[folder].add(pdf_path)
    return folders


def create_folder_reports(
    folders: Dict[str, set[Path]]
) -> Dict[str, Dict[str, List[str]]]:
    folder_reports: Dict[str, Dict[str, List[str]]] = dict()
    for folder, pdf_paths in folders.items():
        folder_reports[folder] = {song: [] for song in REPERTOIRE}
        for pdf_path in pdf_paths:
            song = pdf_path.parts[-2]
            folder_reports[folder][song].append(pdf_path.stem[: -(len(song) + 1)])
    return folder_reports


def propagate_missing_parts(
    folder_reports: Dict[str, Dict[str, List[str]]], folders: Dict[str, set[Path]]
):
    for folder, reports in folder_reports.items():
        for song, parts in reports.items():
            if len(parts) == 0:
                replacements = REPLACEMENTS.get(folder, [])
                for rep in replacements:
                    replacement_songs = {e for e in folders[rep] if song in str(e)}
                    folders[folder] = folders[folder].union(replacement_songs)
                    break
    return folders


def main():
    folders = create_folders()
    folder_reports = create_folder_reports(folders)
    folders = propagate_missing_parts(folder_reports, folders)
    folders = sort_folders(folders)

    # create the pdfs for each folder
    create_folder_pdfs(folders)


if __name__ == "__main__":
    main()
