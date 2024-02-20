## Back-up Rule
* Put input files that you're still working on it in main directory

* Once you obtain a preferable result, put it into directory with date. ex. tcv_axisym/240219

* Only back up input and threed1 onto github.

## How to run

- Procedure

```bash
./replace_paramAC.py --tag {profile} --input input.first_init.vmec --ac_ranges {integer}
./run_dcon.py --tag {profile} 2>/dev/null
./file_manager.py --tag {profile}

./run.py -e -t {profile} --ac_ranges {integer}
# example
./run.py -e -t curr_2p_gs_pres_10e3 --ac_ranges 10 11 30 31 40 41 1 2 3 4 5 6
```

## Parameter setting 
1. aspect ratio ~1.5
2. current $10^5 \to 10^6$  A
3. elongation ~ 2 or 2.5 
4. a= radius 30 or 33 cm (a = (Rmax - Rmin) / 2)
5. 0.1 Tesla ~ plasma current 100kA or more
6. q factor must be larger than 1
