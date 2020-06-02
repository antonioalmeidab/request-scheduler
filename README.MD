# request-scheduler
HTTP application to schedule POST requests using cron and redis.

> Install dependencies 
    Create virtual environment and install dependencies
    `pip install -r requirements.txt`

> Config
    Setup config/config.ini according to example file
    `schedule_path`: Application path
    `env_path`: Virtual env path
    `user`: Linux OS user which will run application

    Go to `request_run.py` and on the following line
    `requests.post('URL', json.dumps(_data))`
    change URL to the desired endpoint
    
> Request example
```json
{
  "profile": Scheduling profile name
  "schedule": {
  	"interval": 1,
  	"time_unit": "days",
  	"time": [OPTIONAL] HH:MM format, mandatory if days or day_month time unit
  },
  "data": { Scheduled request body }
}
```