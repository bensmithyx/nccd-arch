Github is trash and deletes empty directories
To make them again do 
```bash
ls | grep startup | sed 's/.startup//g' | xargs -I % echo %: > lab.dep
```

```bash
ls | grep startup | sed 's/.startup//g' | xargs -I % echo 'placeholder' > %/placeholder
```
