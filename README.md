# VSecureSphere Setup Guide

This guide explains how to set up MongoDB using Docker and run the backend server located in the `ui/backend` folder to access **VSecureSphere**.

---

## 📦 Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed and running
- [Node.js and npm](https://nodejs.org/) installed
- Terminal / Command Prompt access

---

## 🛠 Step 1: Pull MongoDB Docker Image

```bash
docker pull mongo
```

---

## 🚀 Step 2: Run MongoDB Container

```bash
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodbdata:/data/db \
  mongo
```

- Runs MongoDB in detached mode
- Exposes MongoDB on port `27017`
- Uses a Docker volume for persistent data

---

## 📂 Step 3: Navigate to Backend Directory

```bash
cd UI/backend
```

---

## ▶️ Step 4: Install Dependencies and Start Backend Server

```bash
uvicorn main:app --reload
```

Make sure your backend connects to MongoDB at `mongodb://localhost:27017`. Update the `.env` file if needed.

---

## ✅ VSecureSphere is Live!

The backend should now be running and connected to MongoDB. Your **VSecureSphere** system is ready for use from the frontend.


---

## ☸️ Step 5: Install and Start Minikube (For Kubernetes-based Deployment)

### 🧩 Install Minikube

Follow the official guide to install Minikube based on your OS:  
https://minikube.sigs.k8s.io/docs/start/

For quick installation on common platforms:

#### On Ubuntu / Debian:

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

If you're using Kubernetes to deploy VSecureSphere components, you can start Minikube locally:

```bash
minikube start
```

Once Minikube is running, you can deploy your backend and other services to the local Kubernetes cluster.

To check the status:

```bash
minikube status
```

Make sure your Kubernetes manifests or Helm charts are ready for deployment in the Minikube environment.

---

## 🧱 Step 6: Deploy to Kubernetes

Once Minikube is running, you can deploy your backend services using Kubernetes:

```bash
kubectl apply -f <deployment-file>.yaml
kubectl get pods
kubectl get services
```

To expose your service externally (if needed):

```bash
minikube service <service-name>
```

Ensure all your YAML manifests are placed correctly and reference the right Docker images and ports.

---
