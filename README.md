# Capture Bot 

Capture images from Slack

```
@capture-bot capture 
```


## Raspberry Pi

1. install `Raspbian`.
1. `sudo apt-get update`
1. `sudo apt-get upgrade`
1. `sudo apt-get install git`
1. Enable camera from `raspi-config`.
1. Install Docker. 
  
    `curl -sSL https://get.docker.com | sh`

1. Give the ‘pi’ user the ability to run Docker. 
    
    `sudo usermod -aG docker pi`

1. Logout and login again. 
1. Clone this repo.
1. Create env file. `env.txt`

    ```
    API_TOKEN=hoge
    GOOGLE_API_KEY=hoge
    ERRORS_TO=hoge
    IMAGE_SENT_TO=hoge
    ```
1. Start the Docker service. `systemctl start docker.service`
1. `docker build ./ -t capture-bot`
1. `docker run --privileged --env-file ./env.txt capture-bot`

## Tips

### Start on reboot

`capture-bot.sh`

```sh
cd capture-bot
docker build ./ -t capture-bot && docker run --privileged --env-file ./env.txt --restart=always capture-bot
```

`crontab -e`

```sh
@reboot /home/pi/capture-bot.sh
```

