/***************************************************************************
 * The contents of this file were generated with Amplify Studio.           *
 * Please refrain from making any modifications to this file.              *
 * Any changes to this file will be overwritten when running amplify pull. *
 **************************************************************************/

import * as React from "react";
import { GridProps, TextFieldProps } from "@aws-amplify/ui-react";
import { EscapeHatchProps } from "@aws-amplify/ui-react/internal";
export declare type ValidationResponse = {
    hasError: boolean;
    errorMessage?: string;
};
export declare type ValidationFunction<T> = (value: T, validationResponse: ValidationResponse) => ValidationResponse | Promise<ValidationResponse>;
export declare type ProjectsCreateFormInputValues = {
    name?: string;
    updatedDate?: string;
    createdDate?: string;
    rawVideoURL?: string;
    subtitleURL?: string;
    settingURL?: string;
};
export declare type ProjectsCreateFormValidationValues = {
    name?: ValidationFunction<string>;
    updatedDate?: ValidationFunction<string>;
    createdDate?: ValidationFunction<string>;
    rawVideoURL?: ValidationFunction<string>;
    subtitleURL?: ValidationFunction<string>;
    settingURL?: ValidationFunction<string>;
};
export declare type PrimitiveOverrideProps<T> = Partial<T> & React.DOMAttributes<HTMLDivElement>;
export declare type ProjectsCreateFormOverridesProps = {
    ProjectsCreateFormGrid?: PrimitiveOverrideProps<GridProps>;
    name?: PrimitiveOverrideProps<TextFieldProps>;
    updatedDate?: PrimitiveOverrideProps<TextFieldProps>;
    createdDate?: PrimitiveOverrideProps<TextFieldProps>;
    rawVideoURL?: PrimitiveOverrideProps<TextFieldProps>;
    subtitleURL?: PrimitiveOverrideProps<TextFieldProps>;
    settingURL?: PrimitiveOverrideProps<TextFieldProps>;
} & EscapeHatchProps;
export declare type ProjectsCreateFormProps = React.PropsWithChildren<{
    overrides?: ProjectsCreateFormOverridesProps | undefined | null;
} & {
    clearOnSuccess?: boolean;
    onSubmit?: (fields: ProjectsCreateFormInputValues) => ProjectsCreateFormInputValues;
    onSuccess?: (fields: ProjectsCreateFormInputValues) => void;
    onError?: (fields: ProjectsCreateFormInputValues, errorMessage: string) => void;
    onChange?: (fields: ProjectsCreateFormInputValues) => ProjectsCreateFormInputValues;
    onValidate?: ProjectsCreateFormValidationValues;
} & React.CSSProperties>;
export default function ProjectsCreateForm(props: ProjectsCreateFormProps): React.ReactElement;
