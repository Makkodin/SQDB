import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Card, Table } from "react-bootstrap";
import { Link } from "react-router-dom";


function ProjectsID() {


    const { id } = useParams()

    const [ error, setError] = useState(null);
    const [ isLoaded, setIsLoaded] = useState(false);
    const [ project_info, setProjectInfo ] = useState(null);
      
    useEffect(() => {
        fetch(`/projects/${id}`)
            .then((res) => res.json())
            .then(
                (result) => {
                  setIsLoaded(true);
                  setProjectInfo(result);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }, [])// eslint-disable-line react-hooks/exhaustive-deps

    console.log("Project ", id, " content :",project_info)
    let body = <></>;
    let head = <></>;
    

    if (error) {
        return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
        return <div>Loading...</div>;
    } else {
        head = (
            <thead>
                <tr>
                    <th>№</th>
                    <th>Ячейка</th>
                    <th>Тип</th>
                    <th>Подтип</th>

                </tr>
            </thead>
        );

        body = (
            <tbody>
                {project_info.sort().map((item, index) => {
                return (
                    <tr key={item}>
                    <th>{index + 1}</th>
                    <th>
                    <Link to={`/flowcells/${item[0]}`}>
                          <b>{item[0]}</b>
                        </Link>
                    </th>
                    <th>{item[1]}</th>
                    <th>{item[2]}</th>
                    </tr>
                );
                })}
            </tbody>
        );
    }

    return (
        <>
        <Card>
        <h4
            style={{
                marginTop: 25,
                marginBot: 25,
                marginLeft: 25,
                marginRight: 25,
            }}>
        
        Проект :<b> {id}</b>
        </h4>
        </Card>

        <Card>
        <Table bordered hover>
            {head}
            {body}
        </Table>
        
        </Card>
      </>
      
    );
    
}    
export default ProjectsID;
