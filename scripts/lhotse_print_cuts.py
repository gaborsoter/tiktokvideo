from lhotse import CutSet

cuts = CutSet.from_file('cuts.jsonl.gz')

print(cuts)