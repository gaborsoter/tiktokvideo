/***************************************************************************
 * The contents of this file were generated with Amplify Studio.           *
 * Please refrain from making any modifications to this file.              *
 * Any changes to this file will be overwritten when running amplify pull. *
 **************************************************************************/

/* eslint-disable */
import * as React from "react";
import { getOverrideProps } from "@aws-amplify/ui-react/internal";
import { Flex, Icon, Image, View } from "@aws-amplify/ui-react";
export default function HeroLayout2(props) {
  const { overrides, ...rest } = props;
  return (
    <View
      width="1440px"
      height="858px"
      display="block"
      gap="unset"
      alignItems="unset"
      justifyContent="unset"
      position="relative"
      border="1px SOLID rgba(0,0,0,1)"
      padding="0px 0px 0px 0px"
      {...getOverrideProps(overrides, "HeroLayout2")}
      {...rest}
    >
      <View
        width="1440px"
        height="858px"
        display="block"
        gap="unset"
        alignItems="unset"
        justifyContent="unset"
        position="absolute"
        top="0%"
        bottom="0%"
        left="0%"
        right="0%"
        padding="0px 0px 0px 0px"
        backgroundColor="rgba(0,0,0,1)"
        {...getOverrideProps(overrides, "image")}
      ></View>
      <View
        width="1049px"
        height="50px"
        display="block"
        gap="unset"
        alignItems="unset"
        justifyContent="unset"
        position="absolute"
        top="99.18%"
        bottom="-5.01%"
        left="17.22%"
        right="9.93%"
        padding="0px 0px 0px 0px"
        backgroundColor="rgba(0,56,255,1)"
        {...getOverrideProps(overrides, "Rectangle 1164")}
      ></View>
      <Flex
        width="1440px"
        height="858px"
        {...getOverrideProps(overrides, "Contact")}
      ></Flex>
      <Image
        width="10.51%"
        height="31.66%"
        display="block"
        gap="unset"
        alignItems="unset"
        justifyContent="unset"
        position="absolute"
        top="24.94%"
        bottom="43.39%"
        left="58.2%"
        right="31.3%"
        transformOrigin="top left"
        transform="rotate(1.06deg)"
        boxShadow="15px 4px 50px rgba(0.9843137264251709, 1, 0, 1)"
        padding="0px 0px 0px 0px"
        objectFit="unset"
        {...getOverrideProps(overrides, "image 372")}
      ></Image>
      <Image
        width="10.81%"
        height="32.22%"
        display="block"
        gap="unset"
        alignItems="unset"
        justifyContent="unset"
        position="absolute"
        top="33.45%"
        bottom="34.33%"
        left="79.28%"
        right="9.9%"
        transformOrigin="top left"
        transform="rotate(2.84deg)"
        padding="0px 0px 0px 0px"
        objectFit="unset"
        {...getOverrideProps(overrides, "image 374")}
      ></Image>
      <Icon
        width="105.5px"
        height="36.62px"
        viewBox={{ minX: 0, minY: 0, width: 105.5, height: 36.616455078125 }}
        paths={[
          {
            d: "M105.5 36.6165L102.001 13.7891L83.9813 28.2332L105.5 36.6165ZM0.47622 6.05897C46.7318 -5.28112 77.0215 9.2185 92.8746 24.0306L95.6054 21.1079C78.78 5.38723 47.1098 -9.49223 -0.47622 2.17402L0.47622 6.05897Z",
            stroke: "rgba(251,255,0,1)",
            fillRule: "nonzero",
            strokeWidth: 4,
          },
        ]}
        display="block"
        gap="unset"
        alignItems="unset"
        justifyContent="unset"
        position="absolute"
        top="29.76%"
        bottom="65.97%"
        left="70.42%"
        right="22.26%"
        {...getOverrideProps(overrides, "Vector 1")}
      ></Icon>
    </View>
  );
}
