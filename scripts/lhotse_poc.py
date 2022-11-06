from lhotse import CutSet, RecordingSet, align_with_torchaudio, annotate_with_whisper
from tqdm import tqdm

recordings = RecordingSet.from_dir("files", pattern="*.wav")

cuts = annotate_with_whisper(recordings)

cuts_aligned = align_with_torchaudio(cuts)

with CutSet.open_writer("cuts.jsonl.gz") as writer:
    for cut in tqdm(cuts_aligned, desc = "Progress"):
        writer.write(cut)