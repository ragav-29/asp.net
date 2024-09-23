## Istio Notes ##

** Istio Installation **

https://istio.io/latest/docs/setup/getting-started/

- Setting up Istio Ad-Ons

kubectl apply -f samples/addons/

** Create prod namespace **
- kubectl create ns prod
- kubectl apply -n prod java.yml {Deploy below apps in prod Namespace}

** Setup 2 TIER application {Java and Node-js} fetch images from DOCKERHUB

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-image
        image: devopsmela/java-numeric-app
        ports:
        - containerPort: 8080

---
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  ports:
  - port: 8080
  selector:
    app: my-app

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-node-js
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app-node-js
  template:
    metadata:
      labels:
        app: my-app-node-js
    spec:
      containers:
      - name: my-image-node-js
        image: devopsmela/node-js:v1
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: node-service
spec:
  type: NodePort
  ports:
  - port: 5000
  selector:
    app: my-app-node-js

## Test the connectivity ##

curl private-ip:8080/
curl private-ip:8080/compare/51
curl private-ip:8080/increment/51

or test if from the internet by allowing NodePort in inbound rules

## Istio Injection

- kubectl get ns --show-labels {Show Labels}
- kubectl label ns prod istio-injection=enabled

## Monitor Kiali dashboard
- kubectl get svc -n istio-system 
- kubectl edit svc kiali -n istio-system {Edit ServiceType to NodePort}
    "White list Kiali svc NodePort to access the dashboard"
- kubectl rollout -h {To restart deployment}
- kubectl -n prod rollout restart deploy app-deployment

## Send Dummy Traffic's: 
- while true; do curl -s private-ip:8080/increment/99; echo ; sleep 1; done

## Peer Authentication {https://istio.io/latest/docs/reference/config/security/peer_authentication/}

Peer Authentication defines how traffic will be tunneled (or not) to the sidecar

- kubectl get crds {List CRDS - Custom Resource Definition...}
- kubectl apply -f peer_auth.yml
---
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: prod
spec:
  mtls:
    mode: DISABLE
	
- Now check the Kiali dashboard for mTLS status
