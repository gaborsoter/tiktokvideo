/***************************************************************************
 * The contents of this file were generated with Amplify Studio.           *
 * Please refrain from making any modifications to this file.              *
 * Any changes to this file will be overwritten when running amplify pull. *
 **************************************************************************/

import * as React from "react";
import { EscapeHatchProps } from "@aws-amplify/ui-react/internal";
import { FlexProps, IconProps, ImageProps, ViewProps } from "@aws-amplify/ui-react";
export declare type PrimitiveOverrideProps<T> = Partial<T> & React.DOMAttributes<HTMLDivElement>;
export declare type XHeroLayout2OverridesProps = {
    XHeroLayout2?: PrimitiveOverrideProps<ViewProps>;
    image?: PrimitiveOverrideProps<ViewProps>;
    "Rectangle 1164"?: PrimitiveOverrideProps<ViewProps>;
    Contact?: PrimitiveOverrideProps<FlexProps>;
    "image 372"?: PrimitiveOverrideProps<ImageProps>;
    "image 374"?: PrimitiveOverrideProps<ImageProps>;
    "Vector 1"?: PrimitiveOverrideProps<IconProps>;
} & EscapeHatchProps;
export declare type XHeroLayout2Props = React.PropsWithChildren<Partial<ViewProps> & {
    overrides?: XHeroLayout2OverridesProps | undefined | null;
}>;
export default function XHeroLayout2(props: XHeroLayout2Props): React.ReactElement;
