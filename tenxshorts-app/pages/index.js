import { useState, useEffect } from 'react'
import { withAuthenticator, useAuthenticator } from '@aws-amplify/ui-react'
import { Storage, API, Auth } from "aws-amplify"
import { FileUploader, Collection, Image, Card, Button, View, Divider, Heading } from '@aws-amplify/ui-react'

function Home() {
  const [videoKeys, setVideoKeys] = useState([])
  const [videos, setVideos] = useState([])
  const {signOut} = useAuthenticator((context)=>[context.signOut])

  async function callApi(item) {
    const user = await Auth.currentAuthenticatedUser();
    const token = user.signInUserSession.idToken.jwtToken;
    const identityId = user.attributes.sub;

    // Update the user's address attribute with their identityId
    const credentials = await Auth.currentCredentials();
    await Auth.updateUserAttributes(user, {
      'address': credentials.identityId,
    });
  
    const params = {
      body: {
        videoKey: item,
        identityId: identityId
      },
      headers: {
        Authorization: token
      }
    };
  
    const apiData = await API.post('tenxshorts', '/audio', params);
    console.log('apiData:', apiData);
  }

  const fetchVideos = async () => {
    const {results} = await Storage.list('', {level: 'private'})
    console.log(results) 
    setVideoKeys(results)
    const s3Videos = await Promise.all(
      results.map(
        async (video) => await Storage.get(video.key, {level: 'private'})
      )
    )
    setVideos(s3Videos)
  }

  useEffect(() => {
    fetchVideos()
  }, [])

  const onSuccess = (event) => {
    fetchVideos()
  }

  return (
      <div>    
        <FileUploader
          accessLevel="private"
          acceptedFileTypes={["video/*"]}
          variation="drop"
          onSuccess={onSuccess}
        />
        <Collection
          items={videos}
          type="list"
          direction="row"
          gap="20px"
          wrap="nowrap"
        >
          {(item, index) => (
            <Card
              key={index}
              borderRadius="medium"
              maxWidth="20rem"
              variation="outlined"
            >
              <Image
                src={item}
                alt="Glittering stream with old log, snowy mountain peaks tower over a green field."
              />
              <View padding="xs">
                <Divider padding="xs" />
                <Heading padding="medium">{videoKeys[index].key}</Heading>
                <Button onClick={() => callApi(videoKeys[index].key)} variation="primary" isFullWidth>
                  Process video
                </Button>
              </View>
            </Card>
          )}
        </Collection>
        <Button onClick={signOut}>Sign out</Button>      
      </div>
  )
}

export default withAuthenticator(Home)