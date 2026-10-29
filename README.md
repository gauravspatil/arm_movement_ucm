# arm_ucm

Motion-capture data and analysis code for a reach-and-transport arm movement
study, analyzed under the **Uncontrolled Manifold (UCM) hypothesis** — a
motor-control framework for testing whether variability in joint angles (shoulder, elbow, wrist) is
"structured" to protect a task-relevant outcome (e.g. where the hand ends up)
while being allowed to vary freely in directions that don't affect that
outcome.

## The task

Participants sat at a table with **three fixed target locations, A / B / C,
arranged in a triangle**. On each trial they picked up an object from one
location and performed one of three actions:

| Code | Action | Movement signature |
|---|---|---|
| **1** | Do nothing / rest | Little to no object movement — a baseline/null trial |
| **2** | Move the object to a **different** location | Object transported between two different pads (e.g. A→B, B→C, C→A, and their reverses) |
| **3** | Pick the object up and **put it back down in the same place** | A full lift-carry-replace motion, same start and end pad, no net relocation |

Each trial is logged as a 3-token label, e.g. `A 2 B` (start location, action
code, end location) or `C 3 C` (lift-and-replace at location C). These
sequences are what's stored in the `1/` and `2/` trial-order text files, one
line per trial, in the order the trials were presented to that participant.

## What's in the repo

- **`1/`, `2/`** — per-participant trial-order files (`<Name>_<date>_<session>.txt`),
  one 3-token trial label per line (e.g. `B 2 C`), in presentation order.
- **`Part_102_Data/`** — raw per-trial motion capture, as both tab-delimited
  `.txt`/`.data` files and `.csv` exports, one file per trial recording
  (`trial3`–`trial8`). Each row is one time sample; columns capture shoulder
  (3 Euler angles), elbow (1 angle), wrist (3 angles), object position & rotation,
  knuckle position, and an analog trigger/button voltage used to mark trial
  boundaries.
- **`PnP_101_DataFiles/`** — equivalent raw motion-capture trial recordings
  for a different data collection ("PnP_101", trials 1–8).
- **`pnpData/`** — a processed/renamed subset of the raw trial recordings
  ("UserGraphs" files) for Part_101 and Part_102.
- **`data_processing.py`** — loads a single trial's CSV, uses the analog
  trigger signal to find individual trial start/stop boundaries within the
  continuous recording, extracts the 7 joint angles and the object/knuckle
  positions, computes object-to-knuckle distance to detect when the grasp is
  complete, trims each trial to that point, resamples every trial onto a
  common 500-point time base (converted to radians), and stores the result
  per trial (keyed by trial number, with its label and joint-angle time
  series) in a dictionary pickled to `angles_sub2.pickle`.
- **`angles_sub2.pickle`** — the processed joint-angle dataset for subject 2,
  produced by `data_processing.py`.
- **`ucm_calc.py`** — loads `angles_sub2.pickle`, filters to trials matching
  one trial-type label (e.g. `C 3 C`), computes the mean joint-angle
  trajectory across repeats of that trial type, builds a Jacobian-like
  sensitivity vector (`eta`) relating joint-angle changes to the task
  variable using forearm/hand segment lengths scaled from subject height,
  and for every trial and time point decomposes the deviation from the mean
  into a component **parallel** to `eta` (variance that doesn't affect the
  task outcome) and a component **orthogonal** to `eta` (variance that does).
  From these it computes `V_parallel`, `V_orth`, and the UCM ratio
  `UCM = sqrt(V_parallel) / sqrt(V_orth)`.
- **`V_parallel_a/b/c.png`, `V_orth_a/b/c.png`** — plots of the parallel and
  orthogonal variance components over the normalized movement time course,
  for different trial-type conditions (a/b/c), showing whether task-irrelevant
  variance exceeds task-relevant variance during the movement (the UCM
  signature).

