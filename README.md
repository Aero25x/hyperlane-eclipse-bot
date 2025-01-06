Make sure that you have chrome 129 version or lower
130+ not work corretly with proxy



```bash
sudo apt update
sudo apt install build-essential
```

Make wallets.json file and fill it with wallets from you kozel app.

Create proxy.txt file and enter proxy with usernam and passoword like this

```proxy.txt
20.3.5.63:6754:hxjsve:3pzgwoxuvu
20.3.5.63:6754:hxjsve:3pzgwoxuvu
```

run builder

```bash
make init
```

run app

```bash
make run-new
```





