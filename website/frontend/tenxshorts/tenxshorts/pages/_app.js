import '@/styles/globals.css'
import { Amplify } from 'aws-amplify'
import config from '../src/aws-exports'
import { AmplifyProvider } from '@aws-amplify/ui-react'
import { studioTheme } from '../src/ui-components'
import '@aws-amplify/ui-react/styles.css'


Amplify.configure(config)

export default function App({ Component, pageProps }) {
  return <AmplifyProvider theme={studioTheme}>
    <Component {...pageProps} />
    </AmplifyProvider>
}
