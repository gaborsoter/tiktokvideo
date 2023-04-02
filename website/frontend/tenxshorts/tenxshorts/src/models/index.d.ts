import { ModelInit, MutableModel, __modelMeta__, ManagedIdentifier } from "@aws-amplify/datastore";
// @ts-ignore
import { LazyLoading, LazyLoadingDisabled } from "@aws-amplify/datastore";





type EagerProjects = {
  readonly [__modelMeta__]: {
    identifier: ManagedIdentifier<Projects, 'id'>;
    readOnlyFields: 'createdAt' | 'updatedAt';
  };
  readonly id: string;
  readonly name?: string | null;
  readonly updatedDate?: string | null;
  readonly createdDate?: string | null;
  readonly rawVideoURL?: string | null;
  readonly subtitleURL?: string | null;
  readonly settingURL?: string | null;
  readonly createdAt?: string | null;
  readonly updatedAt?: string | null;
}

type LazyProjects = {
  readonly [__modelMeta__]: {
    identifier: ManagedIdentifier<Projects, 'id'>;
    readOnlyFields: 'createdAt' | 'updatedAt';
  };
  readonly id: string;
  readonly name?: string | null;
  readonly updatedDate?: string | null;
  readonly createdDate?: string | null;
  readonly rawVideoURL?: string | null;
  readonly subtitleURL?: string | null;
  readonly settingURL?: string | null;
  readonly createdAt?: string | null;
  readonly updatedAt?: string | null;
}

export declare type Projects = LazyLoading extends LazyLoadingDisabled ? EagerProjects : LazyProjects

export declare const Projects: (new (init: ModelInit<Projects>) => Projects) & {
  copyOf(source: Projects, mutator: (draft: MutableModel<Projects>) => MutableModel<Projects> | void): Projects;
}