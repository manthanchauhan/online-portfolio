# Online Portfolio

# Requirements
1. sign-up with email and password
    * email verification is a must before account creation.
2. log in with email and password
    * redirects the user to `portfolio edit` page
2. Portfolio edit page
    * requires login
    * is an editable version of `portfolio view` page
3. Portfolio view page
    * doesn't requires login
    * this is the portfolio which recruiters will see
4. About Us page
    * to show developer & website details.

## Portfolio
### About 
1. Name
2. Photo
3. Email
4. Phone
5. Profiles (LinkedIn, GitHub, Codechef, Hackerearth, etc)
6. About me (text)

### Education (initially hidden)
1. School
2. Course
3. Score
4. Start & End year

### Skills
1. Section Name
2. List of skills

### Extra Curriculars 
1. List of achievements

### Projects & Work Samples
1. Title
2. Description
3. Images & Video
4. GitHub link
5. Start & End Date
6. Skills Utilized

### Call of Contact
1. Email
2. Phone 
3. Contact
4. Thank you text

## Design Considerations
* Order of these sections should be changeable, except the "About" and "Call of Contact" section.
* Since reads of portfolio will be multiple times greater than writes, we will store user portfolios as static files.
    Which will increase write time but, will reduce load time by about 75%.
