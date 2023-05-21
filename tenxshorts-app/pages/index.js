import { useState, useEffect } from 'react'
import { withAuthenticator, useAuthenticator } from '@aws-amplify/ui-react'
import { Storage, API, Auth } from "aws-amplify"
import { Collection, Image, Card, Button, View, Divider, Heading } from '@aws-amplify/ui-react'
import { StorageManager } from '@aws-amplify/ui-react-storage';

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
  
    const requestInfo = {
      body: {
        videoKey: item
      },
      headers: {
        Authorization: token,
        
      }
    };
  
    const audioApiData = await API.post('tenxshorts', '/audio', requestInfo);
    console.log("Audio extracted")

    const transcribeApiParams = {
      body: {
        videoKey: item
      },
      headers: {
        Authorization: token
      }
    };
  
    const transcribeApiData = await API.post('tenxshorts', '/transcribe', transcribeApiParams);
    console.log("Transcript done")

    const createSubtitleApiParams = {
      body: {
        videoKey: item
      },
      headers: {
        Authorization: token,
      }
    };
  
    const createSubtitleApiData = await API.post('tenxshorts', '/createSubtitle', createSubtitleApiParams);
    console.log("Subtitle created")


  }

  async function callCreateVideo(item) {
    const user = await Auth.currentAuthenticatedUser();
    const token = user.signInUserSession.idToken.jwtToken;
    const identityId = user.attributes.sub;

    // Update the user's address attribute with their identityId
    const credentials = await Auth.currentCredentials();
    await Auth.updateUserAttributes(user, {
      'address': credentials.identityId,
    });

    const burnSubtitlesApiParams = {
      body: {
        videoKey: item
      },
      headers: {
        Authorization: token,
      }
    };
  
    const burnSubtitleApiData = await API.post('tenxshorts', '/burnSubtitles', burnSubtitlesApiParams);
    console.log("Video created")

  }

  async function downloadVideo(item) {
    // Get the signed URL for the S3 file
    const signedUrl = await Storage.get(item, { level: 'private', download: false });
  
    // Create a new anchor element
    const link = document.createElement('a');
  
    // Set the href and download attributes of the link
    link.href = signedUrl;
    link.download = item;
  
    // Append the link to the document body
    document.body.appendChild(link);
  
    // Programmatically click the link to start the download
    link.click();
  
    // Cleanup - remove the link from the body
    document.body.removeChild(link);
  }

  const fetchVideos = async () => {
    const {results} = await Storage.list('', {level: 'private'})

    // Filter out all non-mp4 files
    const mp4Files = results.filter((result) => {
      return result.key.endsWith('.mp4');
    });

    setVideoKeys(mp4Files)
    const s3Videos = await Promise.all(
      mp4Files
        .filter(video => !video.key.includes('videoclips/'))
        .map(async video => await Storage.get(video.key, { level: 'private' }))
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
        <StorageManager
          accessLevel="private"
          acceptedFileTypes={["video/*"]}
          maxFileCount={1}
          processFile={({ file, key }) => {
            const fileParts = key.split('.');
            const ext = fileParts.pop();
            return {
              file,
              // This will prepend a unix timestamp
              // to ensure all files uploaded are unique
              key: `${Date.now()}${fileParts.join('.')}.${ext}`,
            };
          }}
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
                <Button onClick={() => callCreateVideo(videoKeys[index].key)} variation="primary" isFullWidth>
                  Create video
                </Button>
                <Button onClick={() => downloadVideo(videoKeys[index].key)} variation="primary" isFullWidth>
                  Download video
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