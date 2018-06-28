# WolfSheep

The files in this folder are for the Wolf Sheep Predation NetLogo model. New models that will be run with the GA should be given their own directories.

## Files

* WolfSheep.nlogo: The NetLogo model. It is slightly modified from the original NetLogo model, to end the model once either wolves or sheep die out or pass 10,000 agents.
* Input files for the GA for the grass model: 
  * ranges-grass.txt: The valid ranges of the parameters to be learned by the GA
  * unvaried-grass.txt: The constant values for parameters. These parameters cannot also exist in the ranges file used in the GA.
* Input files for the GA for the non-grass model: 
  * ranges.txt: The valid ranges of the parameters to be learned by the GA.
  * unvaried.txt: The constant values for parameters. These parameters cannot also exist in the ranges file used in the GA.

