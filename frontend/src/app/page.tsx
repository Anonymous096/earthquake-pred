"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";
import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Grid,
  Heading,
  Input,
  Select,
  Text,
  VStack,
  useToast,
} from "@chakra-ui/react";

interface FormData {
  latitude: number;
  longitude: number;
  depth: number;
  magType: "mww" | "Mi" | "mb" | "ms" | "md" | "ml";
  cdi: number;
  mmi: number;
  tsunami: number;
  sig: number;
  dmin: number;
  gap: number;
  nst: number;
}

export default function Home() {
  const [prediction, setPrediction] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>();

  const onSubmit = async (data: FormData) => {
    try {
      setIsLoading(true);
      const response = await axios.post("http://localhost:8000/predict", data);
      setPrediction(response.data.predicted_magnitude);
      toast({
        title: "Prediction successful",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: "Error",
        description:
          error instanceof Error ? error.message : "Failed to make prediction",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8}>
        <Heading>Earthquake Magnitude Prediction</Heading>

        <Box as="form" onSubmit={handleSubmit(onSubmit)} w="100%">
          <Grid templateColumns="repeat(2, 1fr)" gap={6}>
            {/* Latitude and Longitude */}
            <FormControl isInvalid={!!errors.latitude}>
              <FormLabel>Latitude (-90 to 90)</FormLabel>
              <Input
                type="number"
                step="any"
                {...register("latitude", {
                  required: "Latitude is required",
                  min: -90,
                  max: 90,
                })}
              />
            </FormControl>

            <FormControl isInvalid={!!errors.longitude}>
              <FormLabel>Longitude (-180 to 180)</FormLabel>
              <Input
                type="number"
                step="any"
                {...register("longitude", {
                  required: "Longitude is required",
                  min: -180,
                  max: 180,
                })}
              />
            </FormControl>

            {/* Depth and Magnitude Type */}
            <FormControl isInvalid={!!errors.depth}>
              <FormLabel>Depth (km)</FormLabel>
              <Input
                type="number"
                step="any"
                {...register("depth", {
                  required: "Depth is required",
                  min: 0,
                })}
              />
            </FormControl>

            <FormControl isInvalid={!!errors.magType}>
              <FormLabel>Magnitude Type</FormLabel>
              <Select
                {...register("magType", {
                  required: "Magnitude type is required",
                })}
              >
                {["mww", "Mi", "mb", "ms", "md", "ml"].map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </Select>
            </FormControl>

            {/* CDI and MMI */}
            <FormControl isInvalid={!!errors.cdi}>
              <FormLabel>CDI (0-12)</FormLabel>
              <Input
                type="number"
                step="any"
                {...register("cdi", {
                  required: "CDI is required",
                  min: 0,
                  max: 12,
                })}
              />
            </FormControl>

            <FormControl isInvalid={!!errors.mmi}>
              <FormLabel>MMI (0-12)</FormLabel>
              <Input
                type="number"
                step="any"
                {...register("mmi", {
                  required: "MMI is required",
                  min: 0,
                  max: 12,
                })}
              />
            </FormControl>

            {/* Tsunami and Significance */}
            <FormControl isInvalid={!!errors.tsunami}>
              <FormLabel>Tsunami (0 or 1)</FormLabel>
              <Select
                {...register("tsunami", {
                  required: "Tsunami flag is required",
                })}
              >
                <option value="0">No (0)</option>
                <option value="1">Yes (1)</option>
              </Select>
            </FormControl>

            <FormControl isInvalid={!!errors.sig}>
              <FormLabel>Significance</FormLabel>
              <Input
                type="number"
                {...register("sig", {
                  required: "Significance is required",
                  min: 0,
                })}
              />
            </FormControl>

            {/* Minimum Distance and Gap */}
            <FormControl isInvalid={!!errors.dmin}>
              <FormLabel>Minimum Distance</FormLabel>
              <Input
                type="number"
                step="any"
                {...register("dmin", {
                  required: "Minimum distance is required",
                  min: 0,
                })}
              />
            </FormControl>

            <FormControl isInvalid={!!errors.gap}>
              <FormLabel>Gap (0-360)</FormLabel>
              <Input
                type="number"
                step="any"
                {...register("gap", {
                  required: "Gap is required",
                  min: 0,
                  max: 360,
                })}
              />
            </FormControl>

            {/* Number of Stations */}
            <FormControl isInvalid={!!errors.nst}>
              <FormLabel>Number of Stations</FormLabel>
              <Input
                type="number"
                {...register("nst", {
                  required: "Number of stations is required",
                  min: 0,
                })}
              />
            </FormControl>
          </Grid>

          <Button
            mt={8}
            colorScheme="blue"
            type="submit"
            isLoading={isLoading}
            w="100%"
          >
            Predict Magnitude
          </Button>
        </Box>

        {prediction !== null && (
          <Box p={6} bg="blue.50" borderRadius="lg" w="100%" textAlign="center">
            <Text fontSize="lg" fontWeight="bold" mb={2}>
              Predicted Magnitude
            </Text>
            <Text fontSize="4xl" color="blue.600">
              {prediction.toFixed(2)}
            </Text>
          </Box>
        )}
      </VStack>
    </Container>
  );
}
