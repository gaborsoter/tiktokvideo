/***************************************************************************
 * The contents of this file were generated with Amplify Studio.           *
 * Please refrain from making any modifications to this file.              *
 * Any changes to this file will be overwritten when running amplify pull. *
 **************************************************************************/

import * as React from "react";
import { EscapeHatchProps } from "@aws-amplify/ui-react/internal";
import { CheckboxFieldProps, FlexProps, RatingProps, SwitchFieldProps } from "@aws-amplify/ui-react";
export declare type PrimitiveOverrideProps<T> = Partial<T> & React.DOMAttributes<HTMLDivElement>;
export declare type GaborComponentOverridesProps = {
    GaborComponent?: PrimitiveOverrideProps<FlexProps>;
    Rating?: PrimitiveOverrideProps<RatingProps>;
    CheckboxField?: PrimitiveOverrideProps<CheckboxFieldProps>;
    SwitchField?: PrimitiveOverrideProps<SwitchFieldProps>;
} & EscapeHatchProps;
export declare type GaborComponentProps = React.PropsWithChildren<Partial<FlexProps> & {
    overrides?: GaborComponentOverridesProps | undefined | null;
}>;
export default function GaborComponent(props: GaborComponentProps): React.ReactElement;
