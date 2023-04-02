/***************************************************************************
 * The contents of this file were generated with Amplify Studio.           *
 * Please refrain from making any modifications to this file.              *
 * Any changes to this file will be overwritten when running amplify pull. *
 **************************************************************************/

import * as React from "react";
import { EscapeHatchProps } from "@aws-amplify/ui-react/internal";
import { FlexProps, TextProps, ViewProps } from "@aws-amplify/ui-react";
export declare type PrimitiveOverrideProps<T> = Partial<T> & React.DOMAttributes<HTMLDivElement>;
export declare type MarketingFooterOverridesProps = {
    MarketingFooter?: PrimitiveOverrideProps<ViewProps>;
    "Rectangle 738"?: PrimitiveOverrideProps<ViewProps>;
    "Copyright @ 10XSHORTS 2023"?: PrimitiveOverrideProps<TextProps>;
    "Frame 405"?: PrimitiveOverrideProps<FlexProps>;
    "Frame 403"?: PrimitiveOverrideProps<FlexProps>;
    Product?: PrimitiveOverrideProps<TextProps>;
    Demo?: PrimitiveOverrideProps<TextProps>;
    Contact?: PrimitiveOverrideProps<TextProps>;
    About?: PrimitiveOverrideProps<TextProps>;
    "Frame 313"?: PrimitiveOverrideProps<FlexProps>;
    "10XSHORTS"?: PrimitiveOverrideProps<TextProps>;
    "Create scroll stopping short videos with AI"?: PrimitiveOverrideProps<TextProps>;
} & EscapeHatchProps;
export declare type MarketingFooterProps = React.PropsWithChildren<Partial<ViewProps> & {
    overrides?: MarketingFooterOverridesProps | undefined | null;
}>;
export default function MarketingFooter(props: MarketingFooterProps): React.ReactElement;
