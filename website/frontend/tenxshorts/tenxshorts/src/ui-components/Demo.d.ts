/***************************************************************************
 * The contents of this file were generated with Amplify Studio.           *
 * Please refrain from making any modifications to this file.              *
 * Any changes to this file will be overwritten when running amplify pull. *
 **************************************************************************/

import * as React from "react";
import { EscapeHatchProps } from "@aws-amplify/ui-react/internal";
import { FlexProps, TextProps, ViewProps } from "@aws-amplify/ui-react";
export declare type PrimitiveOverrideProps<T> = Partial<T> & React.DOMAttributes<HTMLDivElement>;
export declare type DemoOverridesProps = {
    Demo?: PrimitiveOverrideProps<FlexProps>;
    "WATCH FULL DEMO"?: PrimitiveOverrideProps<TextProps>;
    "Rectangle 1167"?: PrimitiveOverrideProps<ViewProps>;
} & EscapeHatchProps;
export declare type DemoProps = React.PropsWithChildren<Partial<FlexProps> & {
    overrides?: DemoOverridesProps | undefined | null;
}>;
export default function Demo(props: DemoProps): React.ReactElement;
