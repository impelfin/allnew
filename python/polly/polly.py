#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from boto3 import client

polly = client("polly", region_name="ap-northeast-2")
response = polly.synthesize_speech(Text="안녕하세요.  서민희 앉아민희 반복하면 스퀏미니 진짜 미니 여자미니 ㅎㅎㅎ", OutputFormat="mp3", VoiceId="Seoyeon")

stream = response.get("AudioStream")

with open('aws_test_tts.mp3', 'wb') as f:
    data = stream.read()
    f.write(data)

cmd = "omxplayer -o both aws_test_tts.mp3"

return_value = os.system(cmd)
print('return value: ', return_value)
