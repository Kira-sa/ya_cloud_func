Облачная функция в yandex cloud для генерации картинки для обоев с минималистичным календарем.


# Calendar Generator

## API

POST ...

Content-Type: application/json

{
  "start_date": "2026-01-01",
  "end_date": "2026-12-31",
  ...
}

| Параметр     | Тип    | Default             |
| ------------ | ------ | ------------------- |
| width        | int    | 1179                |
| height       | int    | 2556                |
| start_date   | date   | 1 Jan current year  |
| end_date     | date   | 31 Dec current year |
| scale        | float  | 1.0                 |
| day_style    | string | circle              |
| circle_ratio | float  | 0.75                |
| padding      | object | ...                 |
| colors       | object | ...                 |
