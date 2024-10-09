--- create the schema for the table
CREATE SCHEMA `video_quiberon`
OPTIONS(
  description="Dataset in order to retrieve the output of the ML model",
  location="EU"
);



-- create a table named_result_ml_bronze with 4 fields frame who is an integer, person_present a boolean, day string and hour also a string in the schema video_quiberon
CREATE TABLE video_quiberon.named_result_ml_bronze (
  frame INT64,
  person_present BOOLEAN,
  day STRING,
  hour STRING
);