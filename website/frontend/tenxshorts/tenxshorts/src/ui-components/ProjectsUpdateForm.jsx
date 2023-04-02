/***************************************************************************
 * The contents of this file were generated with Amplify Studio.           *
 * Please refrain from making any modifications to this file.              *
 * Any changes to this file will be overwritten when running amplify pull. *
 **************************************************************************/

/* eslint-disable */
import * as React from "react";
import { Button, Flex, Grid, TextField } from "@aws-amplify/ui-react";
import { getOverrideProps } from "@aws-amplify/ui-react/internal";
import { Projects } from "../models";
import { fetchByPath, validateField } from "./utils";
import { DataStore } from "aws-amplify";
export default function ProjectsUpdateForm(props) {
  const {
    id: idProp,
    projects: projectsModelProp,
    onSuccess,
    onError,
    onSubmit,
    onValidate,
    onChange,
    overrides,
    ...rest
  } = props;
  const initialValues = {
    name: "",
    updatedDate: "",
    createdDate: "",
    rawVideoURL: "",
    subtitleURL: "",
    settingURL: "",
  };
  const [name, setName] = React.useState(initialValues.name);
  const [updatedDate, setUpdatedDate] = React.useState(
    initialValues.updatedDate
  );
  const [createdDate, setCreatedDate] = React.useState(
    initialValues.createdDate
  );
  const [rawVideoURL, setRawVideoURL] = React.useState(
    initialValues.rawVideoURL
  );
  const [subtitleURL, setSubtitleURL] = React.useState(
    initialValues.subtitleURL
  );
  const [settingURL, setSettingURL] = React.useState(initialValues.settingURL);
  const [errors, setErrors] = React.useState({});
  const resetStateValues = () => {
    const cleanValues = projectsRecord
      ? { ...initialValues, ...projectsRecord }
      : initialValues;
    setName(cleanValues.name);
    setUpdatedDate(cleanValues.updatedDate);
    setCreatedDate(cleanValues.createdDate);
    setRawVideoURL(cleanValues.rawVideoURL);
    setSubtitleURL(cleanValues.subtitleURL);
    setSettingURL(cleanValues.settingURL);
    setErrors({});
  };
  const [projectsRecord, setProjectsRecord] = React.useState(projectsModelProp);
  React.useEffect(() => {
    const queryData = async () => {
      const record = idProp
        ? await DataStore.query(Projects, idProp)
        : projectsModelProp;
      setProjectsRecord(record);
    };
    queryData();
  }, [idProp, projectsModelProp]);
  React.useEffect(resetStateValues, [projectsRecord]);
  const validations = {
    name: [],
    updatedDate: [],
    createdDate: [],
    rawVideoURL: [{ type: "URL" }],
    subtitleURL: [{ type: "URL" }],
    settingURL: [{ type: "URL" }],
  };
  const runValidationTasks = async (
    fieldName,
    currentValue,
    getDisplayValue
  ) => {
    const value =
      currentValue && getDisplayValue
        ? getDisplayValue(currentValue)
        : currentValue;
    let validationResponse = validateField(value, validations[fieldName]);
    const customValidator = fetchByPath(onValidate, fieldName);
    if (customValidator) {
      validationResponse = await customValidator(value, validationResponse);
    }
    setErrors((errors) => ({ ...errors, [fieldName]: validationResponse }));
    return validationResponse;
  };
  const convertToLocal = (date) => {
    const df = new Intl.DateTimeFormat("default", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      calendar: "iso8601",
      numberingSystem: "latn",
      hourCycle: "h23",
    });
    const parts = df.formatToParts(date).reduce((acc, part) => {
      acc[part.type] = part.value;
      return acc;
    }, {});
    return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}`;
  };
  return (
    <Grid
      as="form"
      rowGap="15px"
      columnGap="15px"
      padding="20px"
      onSubmit={async (event) => {
        event.preventDefault();
        let modelFields = {
          name,
          updatedDate,
          createdDate,
          rawVideoURL,
          subtitleURL,
          settingURL,
        };
        const validationResponses = await Promise.all(
          Object.keys(validations).reduce((promises, fieldName) => {
            if (Array.isArray(modelFields[fieldName])) {
              promises.push(
                ...modelFields[fieldName].map((item) =>
                  runValidationTasks(fieldName, item)
                )
              );
              return promises;
            }
            promises.push(
              runValidationTasks(fieldName, modelFields[fieldName])
            );
            return promises;
          }, [])
        );
        if (validationResponses.some((r) => r.hasError)) {
          return;
        }
        if (onSubmit) {
          modelFields = onSubmit(modelFields);
        }
        try {
          Object.entries(modelFields).forEach(([key, value]) => {
            if (typeof value === "string" && value.trim() === "") {
              modelFields[key] = undefined;
            }
          });
          await DataStore.save(
            Projects.copyOf(projectsRecord, (updated) => {
              Object.assign(updated, modelFields);
            })
          );
          if (onSuccess) {
            onSuccess(modelFields);
          }
        } catch (err) {
          if (onError) {
            onError(modelFields, err.message);
          }
        }
      }}
      {...getOverrideProps(overrides, "ProjectsUpdateForm")}
      {...rest}
    >
      <TextField
        label="Name"
        isRequired={false}
        isReadOnly={false}
        value={name}
        onChange={(e) => {
          let { value } = e.target;
          if (onChange) {
            const modelFields = {
              name: value,
              updatedDate,
              createdDate,
              rawVideoURL,
              subtitleURL,
              settingURL,
            };
            const result = onChange(modelFields);
            value = result?.name ?? value;
          }
          if (errors.name?.hasError) {
            runValidationTasks("name", value);
          }
          setName(value);
        }}
        onBlur={() => runValidationTasks("name", name)}
        errorMessage={errors.name?.errorMessage}
        hasError={errors.name?.hasError}
        {...getOverrideProps(overrides, "name")}
      ></TextField>
      <TextField
        label="Updated date"
        isRequired={false}
        isReadOnly={false}
        type="datetime-local"
        value={updatedDate && convertToLocal(new Date(updatedDate))}
        onChange={(e) => {
          let value =
            e.target.value === "" ? "" : new Date(e.target.value).toISOString();
          if (onChange) {
            const modelFields = {
              name,
              updatedDate: value,
              createdDate,
              rawVideoURL,
              subtitleURL,
              settingURL,
            };
            const result = onChange(modelFields);
            value = result?.updatedDate ?? value;
          }
          if (errors.updatedDate?.hasError) {
            runValidationTasks("updatedDate", value);
          }
          setUpdatedDate(value);
        }}
        onBlur={() => runValidationTasks("updatedDate", updatedDate)}
        errorMessage={errors.updatedDate?.errorMessage}
        hasError={errors.updatedDate?.hasError}
        {...getOverrideProps(overrides, "updatedDate")}
      ></TextField>
      <TextField
        label="Created date"
        isRequired={false}
        isReadOnly={false}
        type="datetime-local"
        value={createdDate && convertToLocal(new Date(createdDate))}
        onChange={(e) => {
          let value =
            e.target.value === "" ? "" : new Date(e.target.value).toISOString();
          if (onChange) {
            const modelFields = {
              name,
              updatedDate,
              createdDate: value,
              rawVideoURL,
              subtitleURL,
              settingURL,
            };
            const result = onChange(modelFields);
            value = result?.createdDate ?? value;
          }
          if (errors.createdDate?.hasError) {
            runValidationTasks("createdDate", value);
          }
          setCreatedDate(value);
        }}
        onBlur={() => runValidationTasks("createdDate", createdDate)}
        errorMessage={errors.createdDate?.errorMessage}
        hasError={errors.createdDate?.hasError}
        {...getOverrideProps(overrides, "createdDate")}
      ></TextField>
      <TextField
        label="Raw video url"
        isRequired={false}
        isReadOnly={false}
        value={rawVideoURL}
        onChange={(e) => {
          let { value } = e.target;
          if (onChange) {
            const modelFields = {
              name,
              updatedDate,
              createdDate,
              rawVideoURL: value,
              subtitleURL,
              settingURL,
            };
            const result = onChange(modelFields);
            value = result?.rawVideoURL ?? value;
          }
          if (errors.rawVideoURL?.hasError) {
            runValidationTasks("rawVideoURL", value);
          }
          setRawVideoURL(value);
        }}
        onBlur={() => runValidationTasks("rawVideoURL", rawVideoURL)}
        errorMessage={errors.rawVideoURL?.errorMessage}
        hasError={errors.rawVideoURL?.hasError}
        {...getOverrideProps(overrides, "rawVideoURL")}
      ></TextField>
      <TextField
        label="Subtitle url"
        isRequired={false}
        isReadOnly={false}
        value={subtitleURL}
        onChange={(e) => {
          let { value } = e.target;
          if (onChange) {
            const modelFields = {
              name,
              updatedDate,
              createdDate,
              rawVideoURL,
              subtitleURL: value,
              settingURL,
            };
            const result = onChange(modelFields);
            value = result?.subtitleURL ?? value;
          }
          if (errors.subtitleURL?.hasError) {
            runValidationTasks("subtitleURL", value);
          }
          setSubtitleURL(value);
        }}
        onBlur={() => runValidationTasks("subtitleURL", subtitleURL)}
        errorMessage={errors.subtitleURL?.errorMessage}
        hasError={errors.subtitleURL?.hasError}
        {...getOverrideProps(overrides, "subtitleURL")}
      ></TextField>
      <TextField
        label="Setting url"
        isRequired={false}
        isReadOnly={false}
        value={settingURL}
        onChange={(e) => {
          let { value } = e.target;
          if (onChange) {
            const modelFields = {
              name,
              updatedDate,
              createdDate,
              rawVideoURL,
              subtitleURL,
              settingURL: value,
            };
            const result = onChange(modelFields);
            value = result?.settingURL ?? value;
          }
          if (errors.settingURL?.hasError) {
            runValidationTasks("settingURL", value);
          }
          setSettingURL(value);
        }}
        onBlur={() => runValidationTasks("settingURL", settingURL)}
        errorMessage={errors.settingURL?.errorMessage}
        hasError={errors.settingURL?.hasError}
        {...getOverrideProps(overrides, "settingURL")}
      ></TextField>
      <Flex
        justifyContent="space-between"
        {...getOverrideProps(overrides, "CTAFlex")}
      >
        <Button
          children="Reset"
          type="reset"
          onClick={(event) => {
            event.preventDefault();
            resetStateValues();
          }}
          isDisabled={!(idProp || projectsModelProp)}
          {...getOverrideProps(overrides, "ResetButton")}
        ></Button>
        <Flex
          gap="15px"
          {...getOverrideProps(overrides, "RightAlignCTASubFlex")}
        >
          <Button
            children="Submit"
            type="submit"
            variation="primary"
            isDisabled={
              !(idProp || projectsModelProp) ||
              Object.values(errors).some((e) => e?.hasError)
            }
            {...getOverrideProps(overrides, "SubmitButton")}
          ></Button>
        </Flex>
      </Flex>
    </Grid>
  );
}
