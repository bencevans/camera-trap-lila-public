# LILA (Filtered) Public Datasets

[lila.science](http://lila.science) is home to many camera trap datasets. The list below provides information on the number of images, sequences, locations, categories and bounding boxes annotated in each of the available labelsets. The labelsets available from LILA sometimes include references to imagery that is not publicly available. Generally images that contain humans or other reasons for sensitivity are withheld.

In order to work with these datasets, the metadata often needs to be filtered first to images, annotations and categories that are available. Here two sets of filtered labelsets are produced. The first (Public) filters metadata down to only metadata where imagery exists. The second (Public + References) filters beyond the first by removing any image references where there is no annotation.

If using any of the datasets be sure to see the relevant page on LILA for information on licencing, referencing and background information.

All metadata uses the COCO-CameraTrap format. Some of the original datasets and all of the filtered labelsets are provided as Zipped JSON files.

## Datasets

Jump To Dataset:

- [Caltech Camera Traps](#caltech-camera-traps)
- [Channel Islands Camera Traps](#channel-islands-camera-traps)
- [Desert Lion Conservation Camera Traps](#desert-lion-conservation-camera-traps)
- [ENA24-detection](#ena24-detection)
- [Idaho Camera Traps](#idaho-camera-traps)
- [Island Conservation Camera Traps](#island-conservation-camera-traps)
- [Missouri Camera Traps](#missouri-camera-traps)
- [North American Camera Trap Images](#north-american-camera-trap-images)
- [Ohio Small Animals](#ohio-small-animals)
- [Orinoquía Camera Traps](#orinoquía-camera-traps)
- [SWG Camera Traps 2018-2020](#swg-camera-traps-2018-2020)
- [Snapshot Camdeboo](#snapshot-camdeboo)
- [Snapshot Enonkishu](#snapshot-enonkishu)
- [Snapshot Karoo](#snapshot-karoo)
- [Snapshot Kgalagadi](#snapshot-kgalagadi)
- [Snapshot Kruger](#snapshot-kruger)
- [Snapshot Mountain Zebra](#snapshot-mountain-zebra)
- [Snapshot Serengeti](#snapshot-serengeti)
- [Trail Camera Images of New Zealand Animals](#trail-camera-images-of-new-zealand-animals)
- [WCS Camera Traps](#wcs-camera-traps)
- [Wellington Camera Traps](#wellington-camera-traps)

### Caltech Camera Traps

See details on [lila.science](https://lila.science/datasets/caltech-camera-traps)

#### Image-level annotations

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/caltechcameratraps/labels/caltech_camera_traps.json.zip)|245,118|22|243,100|0|140|181,008|
|**Filtered (Public)**|245,118|22|243,100|0|140|181,008|
|**Filtered (Public + Referenced)**|245,118|22|243,100|0|140|181,008|

#### Bounding box annotations

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/caltechcameratraps/labels/caltech_bboxes_20200316.json)|65,112|22|63,025|65,112|85|27,877|
|**Filtered (Public)**|65,112|20|63,025|65,112|85|27,877|
|**Filtered (Public + Referenced)**|65,112|20|61,945|65,112|85|27,877|

<!--
Unavailable categories:
- `37` cow
- `39` pig
-->

### Channel Islands Camera Traps

See details on [lila.science](https://lila.science/datasets/channel-islands-camera-traps/)

#### Metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/channel-islands-camera-traps/channel-islands-camera-traps.json.zip)|264,321|7|245,529|264,266|73|50,626|
|**Filtered (Public)**|258,295|6|240,458|258,240|73|50,309|
|**Filtered (Public + Referenced)**|258,295|6|240,458|258,240|73|50,309|

<!--
Unavailable categories:
- `1` human
-->

### Desert Lion Conservation Camera Traps

See details on [lila.science](https://lila.science/datasets/desert-lion-conservation-camera-traps/)

#### Metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/desert-lion-camera-traps/desert_lion_camera_traps.json.zip)|63,468|46|63,468|0|1|0|
|**Filtered (Public)**|63,468|46|63,468|0|1|0|
|**Filtered (Public + Referenced)**|63,468|46|63,468|0|1|0|

### ENA24-detection

See details on [lila.science](https://lila.science/datasets/ena24detection)

#### Bounding Boxes

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/ena24/ena24.json)|11,596|23|9,676|11,596|0|0|
|**Filtered (Public)**|9,772|22|8,789|9,772|0|0|
|**Filtered (Public + Referenced)**|9,772|22|8,789|9,772|0|0|

<!--
Unavailable categories:
- `8` Human
-->

### Idaho Camera Traps

See details on [lila.science](https://lila.science/datasets/idaho-camera-traps/)

#### Metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/idaho-camera-traps/idaho-camera-traps.json.zip)|1,551,552|62|1,535,725|0|276|1,034,520|
|**Filtered (Public)**|1,527,750|58|1,513,414|0|276|1,032,276|
|**Filtered (Public + Referenced)**|1,527,750|58|1,513,414|0|276|1,032,276|

<!--
Unavailable categories:
- `1` human
- `13` domestic dog
- `29` vehicle
- `48` horse
-->

### Island Conservation Camera Traps

See details on [lila.science](https://lila.science/datasets/island-conservation-camera-traps/)

#### Metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/islandconservationcameratraps/island_conservation_camera_traps_1.02.zip)|142,341|49|127,410|64,671|123|0|
|**Filtered (Public)**|136,080|48|122,602|58,410|123|0|
|**Filtered (Public + Referenced)**|136,080|48|122,602|58,410|123|0|

<!--
Unavailable categories:
- `8` human
-->

### Missouri Camera Traps

See details on [lila.science](https://lila.science/datasets/missouricameratraps)

#### Metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/missouricameratraps/missouri_camera_traps_set1_1.21.json.zip)|24,682|21|24,673|956|1|1,934|
|**Filtered (Public)**|24,682|21|24,673|956|1|1,934|
|**Filtered (Public + Referenced)**|24,682|21|24,673|956|1|1,934|

### North American Camera Trap Images

See details on [lila.science](https://lila.science/datasets/nacti)

#### Metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/nacti/nacti_metadata.1.14.json.zip)|3,382,215|59|3,382,215|0|678|0|
|**Filtered (Public)**|3,382,215|50|3,382,215|0|678|0|
|**Filtered (Public + Referenced)**|3,382,215|50|3,382,215|0|678|0|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| canis lupus `7` | corvus brachyrhynchos `11` | sylvilagus floridanus `63` | rattus rattus `56` | unidentified rodent `57` |
| unidentified rodent `57` | odocoileus virginianus `47` | unidentified sciurus `58` | sciurus niger `60` | zenaida macroura `70` |
| zenaida macroura `70` |    |    |    |    |
-->

#### Bounding Boxes

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/nacti/nacti_20230920_bboxes.zip)|10,564|5|8,892|10,564|3|0|
|**Filtered (Public)**|10,564|4|8,892|10,564|3|0|
|**Filtered (Public + Referenced)**|10,564|4|8,263|10,564|3|0|

<!--
Unavailable categories:
- `0` empty
-->

### Ohio Small Animals

See details on [lila.science](https://lila.science/datasets/ohio-small-animals/)

#### Metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/osu-small-animals/osu-small-animals.json.zip)|118,554|46|118,554|0|168|23,385|
|**Filtered (Public)**|118,554|46|118,554|0|168|23,385|
|**Filtered (Public + Referenced)**|118,554|46|118,554|0|168|23,385|

### Orinoquía Camera Traps

See details on [lila.science](https://lila.science/datasets/orinoquia-camera-traps/)

#### Metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/orinoquia-camera-traps/orinoquia_camera_traps_metadata.zip)|112,267|58|112,221|0|49|18,402|
|**Filtered (Public)**|0|0|0|0|0|0|
|**Filtered (Public + Referenced)**|0|0|0|0|0|0|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| empty `0` | human `1` | black_agouti `2` | collared_peccary `3` | spixs_guan `4` |
| spixs_guan `4` | rodent `5` | unknown_bird `6` | unknown `7` | giant_anteater `8` |
| giant_anteater `8` | ornate_titi_monkey `9` | lowland_tapir `10` | unknown_armadillo `11` | unknown_squirrel_monkey `12` |
| unknown_squirrel_monkey `12` | puma `13` | southern_tamandua `14` | cattle `15` | south_american_coati `16` |
| south_american_coati `16` | ants `17` | amazonian_motmot `18` | unknown_possum `19` | tayra `20` |
| tayra `20` | spotted_paca `21` | margarita_island_capuchin `22` | giant_armadillo `23` | unknown_capuchin_monkey `24` |
| unknown_capuchin_monkey `24` | unknown_reptile `25` | crab-eating_fox `26` | common_green_iguana `27` | domestic_horse `28` |
| domestic_horse `28` | domestic_dog `29` | unknown_cervid `30` | ocelot `31` | white-tailed_deer `32` |
| white-tailed_deer `32` | salvins_curassow `33` | northern_amazon_red_squirrel `34` | jaguarundi `35` | white-lipped_peccary `36` |
| white-lipped_peccary `36` | unknown_howler_monkey `37` | unknown_turtle `38` | unknown_nightjar `39` | unknown_peccary `40` |
| unknown_peccary `40` | red_brocket_deer `41` | margay `42` | insect `43` | unknown_tayra `44` |
| unknown_tayra `44` | orinoco_agouti `45` | jaguar `46` | bush_dog `47` | unknown_mammal `48` |
| unknown_mammal `48` | crestless_curassow `49` | turkey_vulture `50` | white-browed_guan `51` | neotropical_otter `52` |
| neotropical_otter `52` | fasciated_tiger-heron `53` | coiban_agouti `54` | unknown_weasel `55` | giant_otter `56` |
| giant_otter `56` | capybara `57` |    |    |    |
-->

### SWG Camera Traps 2018-2020

See details on [lila.science](https://lila.science/datasets/swg-camera-traps)

#### Class-level annotations

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/swg-camera-traps/swg_camera_traps.zip)|2,039,657|120|2,039,657|0|982|436,617|
|**Filtered (Public)**|1,858,247|118|1,858,247|0|935|410,454|
|**Filtered (Public + Referenced)**|1,858,247|118|1,858,247|0|935|410,454|

<!--
Unavailable categories:
- `1` ignore
- `36` human
-->

#### Bounding Boxes (with species)

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/swg-camera-traps/swg_camera_traps.bounding_boxes.with_species.zip)|133,837|121|120,321|101,659|915|50,389|
|**Filtered (Public)**|132,596|99|119,282|100,638|913|49,999|
|**Filtered (Public + Referenced)**|132,596|99|119,274|100,638|913|49,999|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| ignore `1` | blurred `2` | problem `13` | human `36` | gray_laughingthrush `48` |
| gray_laughingthrush `48` | red_collared_woodpecker `50` | gibbon `55` | indochinese_green_magpie `67` | common_green_magpie `68` |
| common_green_magpie `68` | francois_langur `69` | mountain_hawk_eagle `77` | rufous_necked_hornbill `91` | invertebrate `94` |
| invertebrate `94` | unidentified_lizard `96` | yellow_bellied_weasel `99` | mountain_imperial_pigeon `102` | striated_heron `110` |
| striated_heron `110` | black_throated_laughingthrush `112` | barred_cuckoo_dove `115` | unidentified_snake `116` | white_tailed_robin `117` |
| white_tailed_robin `117` | grey_headed_canary_flycatcher `120` |    |    |    |
-->

#### Bounding Boxes (just animal/person/vehicle labels)

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/swg-camera-traps/swg_camera_traps.bounding_boxes.no_species.zip)|133,837|4|120,321|101,659|915|50,389|
|**Filtered (Public)**|132,596|3|119,282|100,638|913|49,999|
|**Filtered (Public + Referenced)**|132,596|3|119,274|100,638|913|49,999|

<!--
Unavailable categories:
- `2` person
-->

### Snapshot Camdeboo

See details on [lila.science](https://lila.science/datasets/snapshot-camdeboo)

#### Season 1

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshot-safari/CDB/SnapshotCamdeboo_S1_v1.0.json.zip)|30,717|43|30,551|0|20|12,132|
|**Filtered (Public)**|30,393|42|30,227|0|20|12,024|
|**Filtered (Public + Referenced)**|30,393|42|30,227|0|20|12,024|

<!--
Unavailable categories:
- `1` human
-->

### Snapshot Enonkishu

See details on [lila.science](https://lila.science/datasets/snapshot-enonkishu)

#### Season 1

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshot-safari/ENO/SnapshotEnonkishu_S1_v1.0.json.zip)|30,542|39|29,414|0|16|13,301|
|**Filtered (Public)**|29,558|38|28,544|0|16|12,969|
|**Filtered (Public + Referenced)**|29,558|38|28,544|0|16|12,969|

<!--
Unavailable categories:
- `1` human
-->

### Snapshot Karoo

See details on [lila.science](https://lila.science/datasets/snapshot-karoo)

#### Season 1

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshot-safari/KAR/SnapshotKaroo_S1_v1.0.json.zip)|38,320|38|38,293|0|15|14,889|
|**Filtered (Public)**|38,101|37|38,074|0|15|14,806|
|**Filtered (Public + Referenced)**|38,101|37|38,074|0|15|14,806|

<!--
Unavailable categories:
- `1` human
-->

### Snapshot Kgalagadi

See details on [lila.science](https://lila.science/datasets/snapshot-kgalagadi)

#### Season 1

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshot-safari/KGA/SnapshotKgalagadi_S1_v1.0.json.zip)|10,402|31|10,357|0|20|3,611|
|**Filtered (Public)**|10,267|30|10,222|0|20|3,566|
|**Filtered (Public + Referenced)**|10,267|30|10,222|0|20|3,566|

<!--
Unavailable categories:
- `1` human
-->

### Snapshot Kruger

See details on [lila.science](https://lila.science/datasets/snapshot-kruger)

#### Season 1

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshot-safari/KRU/SnapshotKruger_S1_v1.0.json.zip)|10,637|46|10,604|0|39|4,747|
|**Filtered (Public)**|10,105|45|10,072|0|39|4,568|
|**Filtered (Public + Referenced)**|10,105|45|10,072|0|39|4,568|

<!--
Unavailable categories:
- `1` human
-->

### Snapshot Mountain Zebra

See details on [lila.science](https://lila.science/datasets/snapshot-mountain-zebra)

#### Season 1

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshot-safari/MTZ/SnapshotMountainZebra_S1_v1.0.json.zip)|73,606|54|73,570|0|19|71,688|
|**Filtered (Public)**|73,070|53|73,034|0|19|71,178|
|**Filtered (Public + Referenced)**|73,070|53|73,034|0|19|71,178|

<!--
Unavailable categories:
- `1` human
-->

### Snapshot Serengeti

See details on [lila.science](https://lila.science/datasets/snapshot-serengeti)

#### Season 1

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS01.json.zip)|412,858|61|411,414|0|168|148,226|
|**Filtered (Public)**|407,942|48|406,612|0|168|146,269|
|**Filtered (Public + Referenced)**|407,942|48|406,612|0|168|146,269|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| human `1` | insectspider `49` | duiker `50` | cattle `51` | vulture `52` |
| vulture `52` | steenbok `53` | bat `54` | fire `55` | hyenabrown `56` |
| hyenabrown `56` | wilddog `57` | kudu `58` | pangolin `59` | lioncub `60` |
| lioncub `60` |    |    |    |    |
-->

#### Season 2

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS02.json.zip)|583,228|61|573,200|0|174|204,352|
|**Filtered (Public)**|577,365|47|567,428|0|174|202,263|
|**Filtered (Public + Referenced)**|577,365|47|567,428|0|174|202,263|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| human `1` | reptiles `48` | insectspider `49` | duiker `50` | cattle `51` |
| cattle `51` | vulture `52` | steenbok `53` | bat `54` | fire `55` |
| fire `55` | hyenabrown `56` | wilddog `57` | kudu `58` | pangolin `59` |
| pangolin `59` | lioncub `60` |    |    |    |
-->

#### Season 3

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS03.json.zip)|398,689|61|392,507|0|160|147,299|
|**Filtered (Public)**|394,463|46|388,335|0|160|145,873|
|**Filtered (Public + Referenced)**|394,463|46|388,335|0|160|145,873|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| human `1` | wildcat `42` | reptiles `48` | insectspider `49` | duiker `50` |
| duiker `50` | cattle `51` | vulture `52` | steenbok `53` | bat `54` |
| bat `54` | fire `55` | hyenabrown `56` | wilddog `57` | kudu `58` |
| kudu `58` | pangolin `59` | lioncub `60` |    |    |
-->

#### Season 4

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS04.json.zip)|541,872|61|531,554|0|181|200,595|
|**Filtered (Public)**|538,771|46|528,504|0|181|199,474|
|**Filtered (Public + Referenced)**|538,771|46|528,504|0|181|199,474|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| human `1` | genet `44` | zorilla `45` | insectspider `49` | duiker `50` |
| duiker `50` | cattle `51` | vulture `52` | steenbok `53` | bat `54` |
| bat `54` | fire `55` | hyenabrown `56` | wilddog `57` | kudu `58` |
| kudu `58` | pangolin `59` | lioncub `60` |    |    |
-->

#### Season 5

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS05.json.zip)|839,421|61|827,224|0|178|311,096|
|**Filtered (Public)**|834,951|47|822,793|0|177|309,439|
|**Filtered (Public + Referenced)**|834,951|47|822,793|0|177|309,439|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| human `1` | rodents `41` | insectspider `49` | duiker `50` | cattle `51` |
| cattle `51` | vulture `52` | steenbok `53` | bat `54` | fire `55` |
| fire `55` | hyenabrown `56` | wilddog `57` | kudu `58` | pangolin `59` |
| pangolin `59` | lioncub `60` |    |    |    |
-->

#### Season 6

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS06.json.zip)|466,411|61|462,846|0|191|173,093|
|**Filtered (Public)**|461,961|47|458,417|0|189|171,469|
|**Filtered (Public + Referenced)**|461,961|47|458,417|0|189|171,469|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| human `1` | wildcat `42` | insectspider `49` | duiker `50` | cattle `51` |
| cattle `51` | vulture `52` | steenbok `53` | bat `54` | fire `55` |
| fire `55` | hyenabrown `56` | wilddog `57` | kudu `58` | pangolin `59` |
| pangolin `59` | lioncub `60` |    |    |    |
-->

#### Season 7

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS07.json.zip)|837,043|61|832,153|0|169|304,492|
|**Filtered (Public)**|831,869|48|827,051|0|169|302,563|
|**Filtered (Public + Referenced)**|831,869|48|827,051|0|169|302,563|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| human `1` | insectspider `49` | duiker `50` | cattle `51` | vulture `52` |
| vulture `52` | steenbok `53` | bat `54` | fire `55` | hyenabrown `56` |
| hyenabrown `56` | wilddog `57` | kudu `58` | pangolin `59` | lioncub `60` |
| lioncub `60` |    |    |    |    |
-->

#### Season 8

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS08.json.zip)|989,821|61|980,256|0|203|359,557|
|**Filtered (Public)**|984,897|54|975,394|0|203|357,852|
|**Filtered (Public + Referenced)**|984,897|54|975,394|0|203|357,852|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| human `1` | fire `55` | hyenabrown `56` | wilddog `57` | kudu `58` |
| kudu `58` | pangolin `59` | lioncub `60` |    |    |
-->

#### Season 9

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS09.json.zip)|991,858|61|982,404|0|185|369,307|
|**Filtered (Public)**|986,293|53|977,105|0|185|367,480|
|**Filtered (Public + Referenced)**|986,293|53|977,105|0|185|367,480|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| human `1` | bat `54` | fire `55` | hyenabrown `56` | wilddog `57` |
| wilddog `57` | kudu `58` | pangolin `59` | lioncub `60` |    |
|    |    |    |    |    |
-->

#### Season 10

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS10.json.zip)|693,889|61|685,481|0|167|252,974|
|**Filtered (Public)**|691,099|52|682,736|0|166|252,015|
|**Filtered (Public + Referenced)**|691,099|52|682,736|0|166|252,015|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| human `1` | reptiles `48` | bat `54` | fire `55` | hyenabrown `56` |
| hyenabrown `56` | wilddog `57` | kudu `58` | pangolin `59` | lioncub `60` |
| lioncub `60` |    |    |    |    |
-->

#### Season 11

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiS11.json.zip)|506,455|61|499,401|0|125|188,231|
|**Filtered (Public)**|503,933|60|497,050|0|125|187,419|
|**Filtered (Public + Referenced)**|503,933|60|497,050|0|125|187,419|

<!--
Unavailable categories:
- `1` human
-->

#### All metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengeti_S1-11_v2_1.json.zip)|7,261,545|61|7,178,440|0|225|2,659,222|
|**Filtered (Public)**|7,213,544|60|7,131,425|0|225|2,642,116|
|**Filtered (Public + Referenced)**|7,213,544|60|7,131,425|0|225|2,642,116|

<!--
Unavailable categories:
- `1` human
-->

#### Bounding boxes

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/snapshotserengeti-v-2-0/SnapshotSerengetiBboxes_20190903.json.zip)|146,359|4|82,938|146,359|225|34,166|
|**Filtered (Public)**|145,599|3|81,154|145,599|224|33,498|
|**Filtered (Public + Referenced)**|145,599|3|77,500|145,599|224|33,498|

<!--
Unavailable categories:
- `4` vehicle
-->

### Trail Camera Images of New Zealand Animals

See details on [lila.science](https://lila.science/datasets/nz-trailcams)

#### Metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/nz-trailcams/trail_camera_images_of_new_zealand_animals_1.00.json.zip)|2,453,840|98|2,453,840|0|3,127|0|
|**Filtered (Public)**|2,453,840|97|2,453,840|0|3,127|0|
|**Filtered (Public + Referenced)**|2,453,840|97|2,453,840|0|3,127|0|

<!--
Unavailable categories:
- `0` empty
-->

### WCS Camera Traps

See details on [lila.science](https://lila.science/datasets/wcscameratraps)

#### Class-level annotations

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/wcs/wcs_camera_traps.json.zip)|1,369,991|676|1,369,991|0|3,911|179,579|
|**Filtered (Public)**|1,200,700|673|1,200,700|0|3,769|165,354|
|**Filtered (Public + Referenced)**|1,200,700|673|1,200,700|0|3,769|165,354|

<!--
Unavailable categories:
- `75` human
- `348` end
- `558` motorcycle
-->

#### Bounding Boxes (same classes as the class-level labels)

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/wcs/wcs_20220205_bboxes_with_classes.zip)|429,482|678|298,725|374,270|3,792|63,858|
|**Filtered (Public)**|409,148|608|286,650|357,094|3,758|61,232|
|**Filtered (Public + Referenced)**|409,148|608|286,650|357,094|3,758|61,232|

<!--
Unavailable categories:
|  |  |  |  |  |
|--|--|--|--|--|
| crypturellus undulatus `43` | harpia harpyja `49` | haploxypterus cayanus `61` | caprimulgus sp `63` | human `75` |
| human `75` | turdus tephronotus `84` | enicurus leschenaulti `158` | unknown spider `183` | unknown insect `186` |
| unknown insect `186` | unknown caprimulgidae `189` | aguila `200` | sciurus ignitus `205` | pteronura brasiliensis `207` |
| pteronura brasiliensis `207` | monasa morphoeus `213` | formicarius colma `218` | ciconia maguari `220` | hoploxypterus cayanus `222` |
| hoploxypterus cayanus `222` | cabassous centralis `249` | phaetornis sp `251` | melaenornis pammelaina `266` | atelerix albiventris `280` |
| atelerix albiventris `280` | lanarius funebris `284` | presbytis femoralis `311` | nesocharis capistrata `332` | melocichla mentalis `333` |
| melocichla mentalis `333` | colomys goslingi `335` | andropadus gracilirostris `341` | end `348` | alopochen aegyptiaca `350` |
| alopochen aegyptiaca `350` | streptopelia lugens `357` | dicrurus adsimilis `366` | buteo urubitinga ridgwayi `387` | dicaeum trigonostigma `393` |
| dicaeum trigonostigma `393` | sundasciurus hippurus `411` | erithacus cyane `412` | lophura erythrophthalma `415` | myiophoneus caeruleus `417` |
| myiophoneus caeruleus `417` | herpestes semitorquatus `418` | callosciurus notatus `420` | caracara plancus `423` | rhea americana `429` |
| rhea americana `429` | sheppardia lowei `450` | arborophila sp `479` | rhizomys sumatrensis `494` | bubo sp `499` |
| bubo sp `499` | mustela strigidorsa `509` | nisaetus nanus `517` | trochalopteron milnei `519` | iduna aedon `521` |
| iduna aedon `521` | pomatorhinus mcclellandi `527` | unknown cat `534` | zonatrichia capensis `547` | carpococcyx renauldi `552` |
| carpococcyx renauldi `552` | motorcycle `558` | mazama  temama `571` | reptile `588` | asio madagascariensis `594` |
| asio madagascariensis `594` | haliaeetus vociferoides `602` | coturnix delegorguei `605` | flying insect `608` | eliurus webbi `623` |
| eliurus webbi `623` | millipede `632` | microcebus murinus `635` | arremonops chloronotus `637` | crypturellus cinnamomeus `638` |
| crypturellus cinnamomeus `638` | philander oppossum `639` | spilogale putorius `640` | nyctanassa violacea `643` | ploceus baglafecht `673` |
| ploceus baglafecht `673` | vehicle `676` |    |    |    |
-->

#### Bounding Boxes (just animal/person/vehicle labels)

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/wcs/wcs_20220205_bboxes_no_classes.zip)|429,482|5|298,725|374,270|3,792|63,858|
|**Filtered (Public)**|409,148|3|286,650|357,094|3,758|61,232|
|**Filtered (Public + Referenced)**|409,148|3|286,650|357,094|3,758|61,232|

<!--
Unavailable categories:
- `2` person
- `3` vehicle
-->

### Wellington Camera Traps

See details on [lila.science](https://lila.science/datasets/wellingtoncameratraps)

#### Metadata

||Annotations|Categories|Images|BBoxes|Location IDs|Sequence IDs|
|-|-|-|-|-|-|-|
|[**Original**](https://lilawildlife.blob.core.windows.net/lila-wildlife/wellingtoncameratraps/wellington_camera_traps.json.zip)|270,450|17|270,450|0|215|90,478|
|**Filtered (Public)**|270,450|17|270,450|0|215|90,478|
|**Filtered (Public + Referenced)**|270,450|17|270,450|0|215|90,478|

