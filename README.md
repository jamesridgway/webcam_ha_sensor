# Webcam Home Assistant Sensor

A utility that uses inotify to watch `/dev/video*` to determine if a webcam is being used or not, and reports the 
status as a binary output over MQTT to `homeassistant/binary_sensor/webcam_ha_sensor`.

## Home Assistant Setup

Configure an MQTT-based sensor in your Home Assistant `configuration.yaml` by adding:

    mqtt:
      sensor:
        - name: "Desktop Webcam"
          state_topic: "homeassistant/binary_sensor/webcam_ha_sensor"
          value_template: "{{ value_json.state }}"

The sensor will behave as a binary sensor and will have the value of either `on` or `off`.

## Running webcam_ha_sensor

Create a python environment:

    python3 -m venv venv

Install python requirements:

    ./venv/bin/pip install -r requirements.txt

Copy the example `.env` file and substitute the values as needed.

Use `./run.sh` to start the utility:

    ./run.sh

## Running automatically in the background

Depending on what operating system you are running will depend on what you want to do for this.

I am using Ubuntu; therefore, I have added the utility to the [Startup Applications](https://help.ubuntu.com/stable/ubuntu-help/startup-applications.html.en) that should be run when I log in to my computer.
