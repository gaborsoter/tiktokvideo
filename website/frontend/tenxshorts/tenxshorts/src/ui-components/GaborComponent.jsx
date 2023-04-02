/***************************************************************************
 * The contents of this file were generated with Amplify Studio.           *
 * Please refrain from making any modifications to this file.              *
 * Any changes to this file will be overwritten when running amplify pull. *
 **************************************************************************/

/* eslint-disable */
import * as React from "react";
import { getOverrideProps } from "@aws-amplify/ui-react/internal";
import {
  CheckboxField,
  Flex,
  Rating,
  SwitchField,
} from "@aws-amplify/ui-react";
export default function GaborComponent(props) {
  const { overrides, ...rest } = props;
  return (
    <Flex
      gap="10px"
      direction="column"
      width="695px"
      height="402px"
      justifyContent="center"
      alignItems="flex-start"
      overflow="hidden"
      position="relative"
      padding="10px 10px 10px 10px"
      backgroundColor="rgba(255,255,255,1)"
      {...getOverrideProps(overrides, "GaborComponent")}
      {...rest}
    >
      <Rating
        width="unset"
        height="unset"
        shrink="0"
        size="default"
        {...getOverrideProps(overrides, "Rating")}
      ></Rating>
      <CheckboxField
        width="unset"
        height="unset"
        shrink="0"
        label="Checkbox "
        size="large"
        defaultChecked={true}
        isDisabled={false}
        labelPosition="start"
        {...getOverrideProps(overrides, "CheckboxField")}
      ></CheckboxField>
      <SwitchField
        width="unset"
        height="unset"
        shrink="0"
        label="On"
        size="default"
        defaultChecked={true}
        isDisabled={false}
        labelPosition="start"
        {...getOverrideProps(overrides, "SwitchField")}
      ></SwitchField>
    </Flex>
  );
}
