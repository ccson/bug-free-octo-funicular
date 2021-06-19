# TMDB App

This app is a multi-Docker container web application that transcodes uploaded video files to `.h264` format.

Once the videos are transcoded, it gathers the movie information from [TMDB](https://www.themoviedb.org/) and
displays them on the front page.

These uploaded video files will be named like `<IMDB-ID>.<VIDEO-EXTENSION.` (i.e. `tt0241527.mp4`). Where the IMDB ID
will be used to identify which IMDB movie the video file stores the content of.

## Composition

This app is run with 4 Docker containers that serve as different components of the web application:
* `backend` -> Serves as the backend application server that interacts with the database and transcodes videos. The
    application uses FFMPEG to transcode videos. This
    runs as a Python SQLAlchemy-extended Flask application. A better design pattern may possibly be to have the video
    transcoder application run as a separate Docker container or application, instead of consolidating the
    application server with the video transcoder application.
* `frontend` -> Serves as the frontend user-interface of the web application. This application runs as a React.js
    application.
* `db` -> The PostgreSQL Database that stores all state information, specifically movie-detail information and the
    status of each video transcoding process.
* `filesystem_poller` -> A simple Python application that serves as a watcher/poller that detects for events on the
    file system, specifically, the folder where users upload videos. It detects upload events and triggers the
    downstream tasks of transcoding the video and fetching the movie information from the TMDB database.
    
 
## Implementation Details

* `backend`
    * `Flask` -> I decided to use Flask as my Python-based web framework of choice because Flask tends to be recommended
    as a popular choice for any light-weight, extensible, and micro web applications. If the application were to be
    more heavyweight, then I would have possibly explored other frameworks, like Django.
    * `SQLAlchemy` -> I chose to use SQLAlchemy with Flask, because they help abstract database interactions which
    create optimized SQL queries for better performance. It also makes the code more readable, maintainable, and
    re-usable. It also helps improve security by preventing SQL-injection attacks. And the database abstractions that 
    ORMs introduce can help switching databases easier. Although for this use-case, these benefits are not really 
    applicable, I tend to prefer ORM frameworks when feasible and reasonable.
    * `ffmpeg` -> This multimedia service was recommended by the interviewer to transcode videos.
* `frontend`
    * `React.js` -> This popular web development framework was recommended by the interviewer to host the front end
    user-interface.
* `filesystem_poller`
    * `watcdog` -> [Watchdog](https://pythonhosted.org/watchdog/) is a Python libarary that monitors file system events.
* `db` -> This database service was recommended by the interviewer to store movie details and video transcoding status
    information.

## Usage

### Application Args

Here are 3 required, command-line arguments to the application:
* `UPLOADS_FOLDER` -> The name of the input/source video folder. Please prepend a `/` to the path. This will
    map the folder from your $HOME path to the root of the application filesystem. For example, if you set this to be
    `/uploads`, then this will create a mapped volume from the `$HOME/uploads` path in the local machine to the
    `/uploads` path in the root of the Docker/application filesystem.
* `COMPLETE_FOLDER` -> The name of the target/destination video folder for transcoded video files. Please prepend a `/` to the path.
    This will map the folder from your $HOME path to the root of the application filesystem. For example, if you set this to be
    `/uploads`, then this will create a mapped volume from the `$HOME/uploads` path in the local machine to the
    `/uploads` path in the root of the Docker/application filesystem.
* `BACKEND_URL` -> The URL to the backend application server.
* `TMDB_API_KEY` -> The TMDB V3 API Key to use to authenticate when fetching movie details from the TMDB API

### Running Application Locally

Command to run the application:

```bash
UPLOADS_FOLDER=/uploads \
COMPLETE_FOLDER=/complete \
BACKEND_URL=localhost \
TMDB_API_KEY=XXXXXX \
docker-compose up --build --detach
```
Since we're running this application on our local machines, the URL to the backend application server will be
`localhost`.

Copy a video file to the application source folder:
```bash
cp /path/to/videos/tt0295297.mp4 ~/uploads/tt0295297.mp4
```

### Running Application in AWS EC2

Command to run the application:

```bash
UPLOADS_FOLDER=/uploads \
COMPLETE_FOLDER=/complete \
TMDB_API_KEY=XXXXXX \
BACKEND_URL=$(curl http://169.254.169.254/latest/meta-data/public-hostname) \
docker-compose up --build --detach
```

The `$(curl http://169.254.169.254/latest/meta-data/public-hostname)` is a command to fetch the Public IPV4 DNS
of the EC2 Instance itself. More [information](https://unix.stackexchange.com/questions/24355/is-there-a-way-to-get-the-public-dns-address-of-an-instance) here.

Command to SSH into the AWS EC2 Instance:

```bash
ssh -i /path/to/pem/test.pem \ 
ec2-user@<AWS EC2 INSTANCE PUBLIC DNS>
```

Command to upload files to the AWS EC2 Instance:

```bash
scp -i /path/to/pem/test.pem \ 
/path/to/videos/tt0241527.mp4  \
ec2-user@<AWS EC2 INSTANCE PUBLIC DNS>:~/uploads/tt0241527.mp4
```
