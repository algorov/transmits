<!-- header -->
<div align="center">
  <h1>Transmits</h1>
</div>

## About

Message relay between «Telegram» and «VK».

## How to use

Clone the repository:

``` shell
git clone https://github.com/algorov/transmits
```

Setting up the environment:

``` shell
python3 -m venv env && source env/bin/activate && pip3 install -r requirements.txt
```

Specify the VK and Telegram bot tokens in **.env**:

``` shell
BOT_TOKEN=
BOT_TOKEN_VK=
```

Go to the **src/Server/** directory and start the server:

``` shell
dotnet run
```

Go to the **src/TG/** directory and start the server specifying the address and port:

``` shell
# Example
python3 side.py 127.0.0.1 1234
```

Go to the **src/VKBOT/** directory and start the server specifying the address and port:

``` shell
# Example
python3 main.py 127.0.0.1 1234
```

## Contributors ✨

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/algorov"><img src="https://avatars.githubusercontent.com/u/90800616?v=4?s=100" width="100px;" alt="SEMUL"/><br /><sub><b>SEMUL</b></sub></a><br /><a href="https://github.com/algorov/transmits/commits?author=algorov" title="Telegram side">💻</a></td>
        <td align="center" valign="top" width="14.28%"><a href="https://github.com/nadvista"><img src="https://avatars.githubusercontent.com/u/36456084?v=4?s=100" width="100px;" alt="MusaFairy"/><br /><sub><b>MusaFairy</b></sub></a><br /><a href="https://github.com/algorov/transmits/commits?author=nadvista" title="VK side">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
