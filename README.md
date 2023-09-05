## Commands
### Multiple files
To scan pressure density (output files are catogorized automatically)
```
python3 scan_pressure_profile.py
```

And then run dcon
```
./run_dcon.sh
```

### Test a single file
Just to test specific condition (output files are in current dir.)
```
./xvmec input.first_init.vmec
```

And then run dcon
```
./run_dcon_singlefile.sh
```

Note: input.first_init.vmec is fixed in a certain boundary.
1. aspect ratio ~1.5
2. current $10^5 \to 10^6$  A
3. elongation ~ 2 or 2.5 
4. a= radius 30 or 33 cm (a = (Rmax - Rmin) / 2)
5. 0.1 Tesla ~ plasma current 100kA or more
6. q factor must be larger than 1
