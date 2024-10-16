---
name: Critical Issue
about: The underlying values of the dataset are biased, corrupted, or demonstrably incorrect.
title: '(Critical) '
labels: 'critical'
assignees: ''

---

## Summary
**1-3 sentences describing the issue.**

## Datasets Impacted
**Indicate which netCDF files have the issue, including those you suspect.**

You may use individual file names

    Ex. "sfcWind_day_NorESM2-LM_ssp370-126aer_r9i1p1f1_gn_20500101-20591231.nc"
    
or wildcards to refer to multiple files

    Ex. "sfcWind_day_NorESM2-LM_ssp370-126aer*.nc"
    
or describe the datasets impacted

    Ex. Daily 'sfcWind' for NorESM2, ssp370-126aer, all ensemble members, all time periods.


## Reproducible
**Include code that anyone can run to reproduce the issue. Use placeholders for system-specific paths. If you are unable to include code, qualitatively describe how you discovered the issue.**

## Implications
**Describe in detail the implications of this issue. How did it impact your analysis and how could it potentially affect other users?**