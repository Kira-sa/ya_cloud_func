# Настройка CI/CD между Yandex Cloud Functions и GitHub

GitHub дает возможность хранить код функции [Yandex Cloud Functions](https://yandex.cloud/ru/docs/functions/) и развертывать новые версии функции при изменениях в репозитории.

Для этого необходимо настроить CI/CD между Cloud Functions и GitHub с помощью федерации сервисных аккаунтов [Yandex Identity and Access Management](https://yandex.cloud/ru/docs/iam/) и развернуть функции Cloud Functions через запуск рабочих процессов GitHub Actions.

Все шаги описаны в [практическом руководстве](https://yandex.cloud/ru/docs/tutorials/serverless/ci-cd-github-functions). В этом репозитории расположен код функции, описание зависимостей и файлы рабочих процессов.

# Полезные материалы

- [Репозиторий yc-sls-function, в котором реализован GitHub Actions, используемый в workflows](https://github.com/yc-actions/yc-sls-function/blob/main/action.yml).
- [Статья об использовании GitHub Actions](https://nikolaymatrosov.ru/2021-11-08-Building-CI-CD-in-Yandex-Cloud-using-GitHub-Actions/).
- [GitHub Actions, помогающий разобраться в проблемах аутентификации через OpenID Connect](https://github.com/github/actions-oidc-debugger).
- [Статья о том, как работает авторизация в Yandex Cloud и как можно создавать привязки сервисных аккаунтов к федерациям](https://nikolaymatrosov.ru/2025-05-04-Authorizing-in-GitHub-Actions-via-Workload-Identities/).
