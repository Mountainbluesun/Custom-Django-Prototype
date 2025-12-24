# Tests legacy / à revoir

## xfail (assumés)
- tests/test_companies_service.py::test_company_crud_service
  - Legacy JSON -> ORM: API service changée

- tests/test_alerts_views_web.py::test_alerts_user_scoped
  - Scope user/company pas encore implémenté

## anciens skip (convertis en xfail)
- tests/test_set_password.py
  - service à corriger

- tests/test_login.py
  - session Django à revoir

- tests/test_logout.py
  - fonction à revoir

- tests/test_products_csv.py
  - import/export CSV à revoir
