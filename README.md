Github is trash and deletes empty directories
ensures lab.dep has everything opening in parallel
```bash
ls | grep startup | sed 's/.startup//g' | xargs -I % echo %: > lab.dep
```
creates placeholders in all directories to prevent them being deleted causing machines not to work properly
```bash
for i in $(find . -maxdepth 1 -type d); do echo 'placeholder' > $i/placeholder; done
```
delete placeholders if needed
```bash
find . -name "placeholder" -type f -delete
```
