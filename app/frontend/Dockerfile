#------------------------
# Build Env
#------------------------
FROM node:14.17.1-alpine as build

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent

COPY . ./

## Copy .env file and shell script to container
ARG REACT_APP_BACKEND_URL
ENV REACT_APP_BACKEND_URL $REACT_APP_BACKEND_URL
RUN touch .env
RUN echo "REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL" >> .env

RUN npm run build-prod

#------------------------
# Production Env
#------------------------
FROM nginx:stable-alpine

# Static build
COPY --from=build /app/dist /usr/share/nginx/html
COPY --from=build /app/public /usr/share/nginx/html

## Add bash
RUN apk add --no-cache bash

# Default port exposure
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
