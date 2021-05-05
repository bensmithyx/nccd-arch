Github is trash and deletes empty directories
To make them again do 
```bash
ls | grep startup | sed 's/.startup//g' | xargs -I % echo %: > lab.dep
```

```bash
for i in $(find . -maxdepth 1 -type d); do echo 'placeholder' > $i/placeholder; done
```
```bash
find . -name "placeholder" -delete
```
