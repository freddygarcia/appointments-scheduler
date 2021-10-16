
This project is intended to be an ideal approach to the Appointment Scheduler Tango coding challenge.

## Starting the service

To run this service you have multiple alternatives:

 
#### Running the public docker image with the following command:
 
-  `docker run --rm -p 5000:5000 zoren101/appointment:latest`

#### Building your own image locally:
- `docker build . -t appointment`
- `docker run --rm -p 5000:5000 appointment`

#### Directly running the project:
- First install the dependencies: `pip install -r requirements.txt`
- Run the flask project: `flask run`
  
 ## Getting Started

### Creating new appointment
We are able to create appointments by doing a POST request to `/appointments`:

##### Request Type:
	JSON

##### Parameters
- user_id: string
- date: string (format: YYYY-MM-DD)
- time: string (format: MM:HH)


```
$ curl http://172.17.0.2:5000/appointments -X POST -d '{"user_id":"freddie", "date" : "2002-01-22", "time"  : "12:30"}' --header "Content-Type: application/json"
```


### Retrieving an appointment

We can get the list of all appointments created for an user doing a GET request to `/appointments`.
The list of appointments are sorted by date.

##### Request Type:
	Plain Text
##### Parameters
- user_id: string
- format: string (optional, json by default)
```
$ curl http://172.17.0.2:5000/appointments/freddie
[{"date":"2002-01-22","time":"12:30:00"}]
```

### Retrieving appointments using multiple formats

```
# JSON (by default)
$ curl http://172.17.0.2:5000/appointments/freddie/cmn
[{"date":"2002-01-22","time":"12:30:00"}]

# ISO
$ curl http://172.17.0.2:5000/appointments/freddie/iso
["2002-01-22T12:30:00"]

# Easier to read
$ curl http://172.17.0.2:5000/appointments/freddie/cmn
["2002-01-22 12:30"]

# Timestamp
$ curl http://172.17.0.2:5000/appointments/freddie/ts
[1011702600.0]
```

### Error handling

#### Unable to create to appointments for the same user in the same date

```
$ curl http://172.17.0.2:5000/appointments -X POST -d '{"user_id":"freddie", "date" : "2002-01-22", "time"  : "12:30"}' --header "Content-Type: application/json"
$ curl http://172.17.0.2:5000/appointments -X POST -d '{"user_id":"freddie", "date" : "2002-01-22", "time"  : "12:30"}' --header "Content-Type: application/json"
{"error":"User freddie has alredy  an appointment on 2002-01-22"}
```


#### Only allowed 30 minutes range time

```
$ curl http://172.17.0.2:5000/appointments -X POST -d '{"user_id":"freddie", "date" : "2001-01-22", "time"  : "12:34"}' --header "Content-Type: application/json"
{"error":"Invalid time: 12:34, please use the format HH:MM in 30 minutes range. e.x. 1:30"}
```


### Other considerations: 

#### Appointments are returned sorted by date

```

$ curl http://172.17.0.2:5000/appointments -X POST -d '{"user_id":"freddie", "date" : "1999-03-22", "time"  : "12:30"}' --header "Content-Type: application/json"
$ curl http://172.17.0.2:5000/appointments -X POST -d '{"user_id":"freddie", "date" : "2001-02-22", "time"  : "12:30"}' --header "Content-Type: application/json"
$ curl http://172.17.0.2:5000/appointments -X POST -d '{"user_id":"freddie", "date" : "2001-03-22", "time"  : "12:30"}' --header "Content-Type: application/json"
$ curl http://172.17.0.2:5000/appointments -X POST -d '{"user_id":"freddie", "date" : "2000-03-22", "time"  : "12:30"}' --header "Content-Type: application/json
$ curl http://172.17.0.2:5000/appointments/freddie/cmn
[
	"1999-03-22 12:30",
	"2000-03-22 12:30",
	"2001-02-22 12:30",
	"2001-03-22 12:30",
	"2002-01-22 12:30"
]
``` 


#### Final notes

I had fun doing this. If I'd have more time, I'd add more date input and output formats, and a better Readme.md 
