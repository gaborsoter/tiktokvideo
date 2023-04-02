/***************************************************************************
 * The contents of this file were generated with Amplify Studio.           *
 * Please refrain from making any modifications to this file.              *
 * Any changes to this file will be overwritten when running amplify pull. *
 **************************************************************************/

/* eslint-disable */
import * as React from "react";
import { getOverrideProps } from "@aws-amplify/ui-react/internal";
import { Flex, Text, View } from "@aws-amplify/ui-react";
export default function Demo(props) {
  const { overrides, ...rest } = props;
  return (
    <Flex
      gap="77px"
      direction="column"
      width="1440px"
      height="910px"
      justifyContent="flex-start"
      alignItems="center"
      position="relative"
      padding="176px 140px 176px 140px"
      backgroundColor="rgba(0,0,0,1)"
      {...getOverrideProps(overrides, "Demo")}
      {...rest}
    >
      <Text
        fontFamily="My Font"
        fontSize="60px"
        fontWeight="500"
        color="rgba(255,255,255,1)"
        lineHeight="19px"
        textAlign="center"
        display="block"
        direction="column"
        justifyContent="unset"
        width="984px"
        height="unset"
        gap="unset"
        alignItems="unset"
        shrink="0"
        position="relative"
        padding="0px 0px 0px 0px"
        whiteSpace="pre-wrap"
        children="WATCH FULL DEMO"
        {...getOverrideProps(overrides, "WATCH FULL DEMO")}
      ></Text>
      <View
        width="863px"
        height="475px"
        display="block"
        gap="unset"
        alignItems="unset"
        justifyContent="unset"
        shrink="0"
        position="relative"
        border="4px SOLID rgba(255,255,255,1)"
        padding="0px 0px 0px 0px"
        backgroundColor="rgba(0,0,0,1)"
        {...getOverrideProps(overrides, "Rectangle 1167")}
      ></View>
    </Flex>
  );
}
