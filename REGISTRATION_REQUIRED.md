# Datasets that require manual registration

The automated download (`scripts/download_real_data.py`) pulls everything that
is publicly retrievable without an account. Three additional datasets would
meaningfully improve training — but all of them sit behind registration walls
we cannot clear automatically.

Drop the files into the paths below exactly as written, and the existing
processors in `src/data/processors.py` will pick them up on the next run of
`python train.py --config config.yaml`.

---

## 1. CodeWorkout — real CS1 Java student data (ProgSnap2 format)

**Why this matters:** this is the single biggest upgrade available. It replaces
the synthesized `data/progsnap2/MainTable.csv` with *real* CS1 Java student
debugging sessions, so the Behavioral RNN and the COKE cognitive chains learn
from actual novice behavior instead of synthetic patterns.

**Steps**

1. Create a free account: <https://pslcdatashop.web.cmu.edu>
2. Browse to **Datasets → Access public datasets**; look for
   "CodeWorkout data, Fall 2019" (or any CodeWorkout release).
3. Click **Request access** and accept the data-use agreement.
4. After approval, download the **ProgSnap2 CSV bundle**.
5. Extract so that the file layout is:
   ```
   data/progsnap2/
       MainTable.csv          <- ~50–200 MB, real CS1 Java events
       DatasetMetadata.json
   ```
6. Remove or rename the synthesized MainTable.csv that is already there:
   ```bash
   mv data/progsnap2/MainTable.csv data/progsnap2/MainTable_synthetic.csv
   ```
   Then place the real one as `MainTable.csv`. `ProgSnap2Processor` will pick
   it up automatically.

---

## 2. Blackbox / BlueJ — 100 M+ Java novice sessions

**Why this matters:** the largest novice-Java behavioral corpus in existence.
Useful if you want to go beyond CodeWorkout-scale and train serious behavioral
models.

**Steps**

1. Read the agreement: <https://bluej.org/blackbox/>
2. Email **`blackbox@bluej.org`** from an institutional address, stating
   your research use case. Response time is typically 1–2 weeks.
3. Once the agreement is signed you receive SSH credentials to a PostgreSQL
   dump + anonymised CSV exports.
4. Export the relevant session tables into ProgSnap2 shape. The mapping is
   straightforward — the `src/data/processors.py` `ProgSnap2Processor` looks
   for `SubjectID`, `ProblemID`, `EventType`, `ServerTimestamp`,
   `CodeStateSection`, `Score`.
5. Save as `data/progsnap2/MainTable.csv`.

---

## 3. Full IBM Project CodeNet (optional)

**Why this matters:** our automated pipeline already pulls a CodeNet Java
subset (~300 accepted submissions via `yangccccc/codenet_after_java` on
Hugging Face) plus CodeSearchNet-Java (~8,000 real functions) plus Defects4J
bug/fix pairs — in total ~9,000 real Java files. The full CodeNet adds 14 M
submissions across 55 languages, which is overkill for a Java-focused CS1
ontology but useful if you want cross-language transfer.

**Steps**

1. Register at: <https://developer.ibm.com/exchanges/data/all/project-codenet/>
2. Download `Project_CodeNet.tar.gz` (~100 GB) to local disk.
3. Extract and copy **only** the Java portion:
   ```bash
   tar -xzf Project_CodeNet.tar.gz
   cp -r Project_CodeNet/data/*/Java data/codenet/java_full/
   ```
4. In `config.yaml`, point the CodeNet path at the larger dir:
   ```yaml
   data:
     datasets:
       codenet:
         enabled: true
         path: "data/codenet_full"
         languages: ["java"]
         max_samples: 50000
   ```

---

## 4. MOOCCubeX (not needed for Java goal)

MOOCCubeX is a course-concept knowledge graph — it is not Java-specific and is
**disabled by default** in `config.yaml`. Leave it disabled unless you are
extending the system to cross-course recommendation.

If you do want it: registration through Tsinghua KEG lab at
<https://github.com/THU-KEG/MOOC-Cube>. The `MOOCCubeXProcessor` in
`src/data/processors.py` expects `entities.json` and `relations.json` in
`data/moocsxcube/`.

---

## What the automated pipeline already provides

| Source | Content | Location |
|---|---|---|
| Hugging Face `yangccccc/codenet_after_java` | 200 real CodeNet Java accepted submissions | `data/codenet/java/correct/cn_*.java` |
| Hugging Face `rufimelo/defects4j` | 467 real Java bug/fix pairs from open-source projects | `data/codenet/java/{correct,buggy}/d4j_*.java` |
| Hugging Face `Nan-Do/code-search-net-java` | 8,000 real Java functions from GitHub | `data/codenet/java/correct/csn_*.java` |
| Synthesized (schema-accurate) | 54,000 CS1 debugging events, 400 subjects | `data/progsnap2/MainTable.csv` |
| Hand-curated in repo | Java misconception ontology | `data/pedagogical_kg/*.json` |

Total on-disk after `python scripts/download_real_data.py`:
- **~9,100 real Java source files** labeled correct/buggy
- **~2,200 aggregated CS1 sessions** (synthetic events, real schema)
- **Java-specific misconception KG** (hand-curated, no download needed)

That is enough to train HVSAE + the misconception classifier head + the
Behavioral RNN on a Java ontology. Swapping the synthesized ProgSnap2 for a
real CodeWorkout drop-in (see section 1) is the highest-value upgrade.
