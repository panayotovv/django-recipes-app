<div align="center">

<img src="https://img.shields.io/badge/MyCook-🍳-orange?style=for-the-badge&labelColor=1a1a1a&color=ff6b35" alt="MyCook" height="40"/>

# 🍳 MyCook

**Discover, save, and share recipes you love.**

[![Made With](https://img.shields.io/badge/Made%20with-❤️%20%26%20JavaScript-red?style=flat-square)](https://github.com)
[![REST API](https://img.shields.io/badge/REST-API-blue?style=flat-square)](https://github.com)
[![Auth](https://img.shields.io/badge/Auth-JWT-green?style=flat-square)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[Live Demo](#) · [Report Bug](issues) · [Request Feature](issues)

---

</div>

## 📖 About

**MyCook** is a full-stack recipe web application where food lovers can browse a curated feed of recipes, like their favorites, and manage a personal profile. Built with a clean REST API backend and a responsive frontend, MyCook makes cooking inspiration effortless.

---

## ✨ Features

- 🔐 **User Authentication** — Secure sign up, log in, and log out with hashed passwords and JWT sessions
- 🍽️ **Recipe Feed** — Browse a rich collection of recipes with images, ingredients, and step-by-step instructions
- ❤️ **Like Recipes** — Save your favorite recipes with a single click; likes are synced to your account
- 👤 **Profile Page** — View your account info and all the recipes you've liked in one place
- 🔌 **REST API** — Full API layer powering every feature, ready for third-party integration

---

## 🖥️ Screenshots

> _Add your screenshots here_

| Feed | Recipe Detail | Profile |
|------|--------------|---------|
| ![feed](#) | ![recipe](#) | ![profile](#) |

---

## 🔌 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register` | Register a new user |
| `POST` | `/api/auth/login` | Log in and receive a token |
| `POST` | `/api/auth/logout` | Invalidate current session |

### Recipes
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/recipes` | Get all recipes |
| `GET` | `/api/recipes/:id` | Get a single recipe |
| `POST` | `/api/recipes` | Create a new recipe _(auth required)_ |
| `PUT` | `/api/recipes/:id` | Update a recipe _(auth required)_ |
| `DELETE` | `/api/recipes/:id` | Delete a recipe _(auth required)_ |

### Likes
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/recipes/:id/like` | Like a recipe _(auth required)_ |
| `DELETE` | `/api/recipes/:id/like` | Unlike a recipe _(auth required)_ |
| `GET` | `/api/recipes/:id/likes` | Get like count for a recipe |

### Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/users/:id` | Get a user's public profile |
| `GET` | `/api/users/:id/liked` | Get all recipes liked by a user |
| `PUT` | `/api/users/:id` | Update profile info _(auth required)_ |

---



