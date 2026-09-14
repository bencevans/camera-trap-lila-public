# LILA (Filtered) Public Datasets

[lila.science](http://lila.science) is home to many camera trap datasets. The list below provides information on the number of images, sequences, locations, categories and bounding boxes annotated in each of the available labelsets. The labelsets available from LILA sometimes include references to imagery that is not publicly available. Generally images that contain humans or other reasons for sensitivity are withheld.

In order to work with these datasets, the metadata often needs to be filtered first to images, annotations and categories that are available. Here two sets of filtered labelsets are produced both of which are filtered to just images (those that can be opened by Python's Pillow library). The first (Public) filters metadata down to only metadata where imagery exists. The second (Public + References) filters beyond the first by removing any image references where there is no annotation.

If using any of the datasets be sure to see the relevant page on LILA for information on licencing, referencing and background information.

Metadata uses COCO/COCO-CameraTrap-style JSON; unlabeled splits may contain only image records. Some of the original datasets and all of the filtered labelsets are provided as Zipped JSON files.
