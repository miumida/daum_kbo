from homeassistant.const import Platform

DOMAIN  = 'daum_kbo'
VERSION = '1.0.0'
TITLE   = "다음스포츠 KBO리그"

PLATFORMS: list[Platform] = [Platform.SENSOR]

BSE_URL = "https://sports.daum.net/prx/hermes/api/team/rank.json?leagueCode=kbo&seasonKey=2025&page=1&pageSize=100"