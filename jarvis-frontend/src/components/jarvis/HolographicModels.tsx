import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Float, MeshTransmissionMaterial } from "@react-three/drei";
import * as THREE from "three";

// Iron Man Helmet Wireframe
const HelmetModel = ({ position, scale = 1 }: { position: [number, number, number]; scale?: number }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.3;
      groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.2) * 0.1;
    }
  });

  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
      <group ref={groupRef} position={position} scale={scale}>
        {/* Helmet main shape - approximated with geometry */}
        <mesh>
          <sphereGeometry args={[0.5, 16, 12, 0, Math.PI * 2, 0, Math.PI * 0.7]} />
          <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.6} />
        </mesh>
        
        {/* Face plate */}
        <mesh position={[0, -0.1, 0.35]} rotation={[0.3, 0, 0]}>
          <planeGeometry args={[0.6, 0.4, 4, 3]} />
          <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.8} />
        </mesh>
        
        {/* Eye slits */}
        <mesh position={[-0.15, 0.05, 0.48]}>
          <boxGeometry args={[0.15, 0.05, 0.02, 2, 1, 1]} />
          <meshBasicMaterial color="#00ffff" wireframe transparent opacity={0.9} />
        </mesh>
        <mesh position={[0.15, 0.05, 0.48]}>
          <boxGeometry args={[0.15, 0.05, 0.02, 2, 1, 1]} />
          <meshBasicMaterial color="#00ffff" wireframe transparent opacity={0.9} />
        </mesh>
        
        {/* Chin piece */}
        <mesh position={[0, -0.35, 0.2]} rotation={[-0.5, 0, 0]}>
          <boxGeometry args={[0.3, 0.2, 0.15, 3, 2, 2]} />
          <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.5} />
        </mesh>
      </group>
    </Float>
  );
};

// Arc Reactor 3D Model
const ArcReactor3D = ({ position, scale = 1 }: { position: [number, number, number]; scale?: number }) => {
  const groupRef = useRef<THREE.Group>(null);
  const innerRingRef = useRef<THREE.Mesh>(null);
  const outerRingRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.z = state.clock.elapsedTime * 0.5;
    }
    if (innerRingRef.current) {
      innerRingRef.current.rotation.z = -state.clock.elapsedTime * 0.8;
    }
    if (outerRingRef.current) {
      outerRingRef.current.rotation.z = state.clock.elapsedTime * 0.3;
    }
  });

  return (
    <Float speed={1.5} rotationIntensity={0.3} floatIntensity={0.8}>
      <group ref={groupRef} position={position} scale={scale}>
        {/* Outer ring */}
        <mesh ref={outerRingRef}>
          <torusGeometry args={[0.5, 0.05, 8, 32]} />
          <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.5} />
        </mesh>
        
        {/* Middle ring */}
        <mesh ref={innerRingRef}>
          <torusGeometry args={[0.35, 0.04, 6, 24]} />
          <meshBasicMaterial color="#00ffff" wireframe transparent opacity={0.7} />
        </mesh>
        
        {/* Inner core */}
        <mesh>
          <cylinderGeometry args={[0.2, 0.2, 0.1, 12, 1]} />
          <meshBasicMaterial color="#ffffff" wireframe transparent opacity={0.8} />
        </mesh>
        
        {/* Core glow */}
        <mesh>
          <sphereGeometry args={[0.15, 8, 8]} />
          <meshBasicMaterial color="#00ffff" transparent opacity={0.3} />
        </mesh>
        
        {/* Triangular segments */}
        {[0, 60, 120, 180, 240, 300].map((angle, i) => (
          <mesh key={i} rotation={[0, 0, (angle * Math.PI) / 180]} position={[0, 0, 0.02]}>
            <planeGeometry args={[0.08, 0.25, 1, 3]} />
            <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.6} side={THREE.DoubleSide} />
          </mesh>
        ))}
      </group>
    </Float>
  );
};

// Gauntlet/Hand Model
const GauntletModel = ({ position, scale = 1 }: { position: [number, number, number]; scale?: number }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.4;
      groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.2;
    }
  });

  return (
    <Float speed={1.8} rotationIntensity={0.4} floatIntensity={1.2}>
      <group ref={groupRef} position={position} scale={scale}>
        {/* Palm base */}
        <mesh>
          <boxGeometry args={[0.4, 0.5, 0.15, 4, 5, 2]} />
          <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.6} />
        </mesh>
        
        {/* Repulsor center */}
        <mesh position={[0, 0, 0.08]}>
          <circleGeometry args={[0.1, 16]} />
          <meshBasicMaterial color="#00ffff" transparent opacity={0.8} />
        </mesh>
        
        {/* Fingers */}
        {[-0.12, -0.04, 0.04, 0.12].map((x, i) => (
          <group key={i} position={[x, 0.35, 0]}>
            <mesh>
              <boxGeometry args={[0.06, 0.2, 0.1, 1, 3, 1]} />
              <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.5} />
            </mesh>
            <mesh position={[0, 0.15, 0]}>
              <boxGeometry args={[0.05, 0.15, 0.08, 1, 2, 1]} />
              <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.5} />
            </mesh>
          </group>
        ))}
        
        {/* Thumb */}
        <mesh position={[-0.25, 0.1, 0]} rotation={[0, 0, 0.5]}>
          <boxGeometry args={[0.06, 0.18, 0.1, 1, 2, 1]} />
          <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.5} />
        </mesh>
      </group>
    </Float>
  );
};

// Hexagonal Tech Panel
const HexPanel = ({ position, scale = 1 }: { position: [number, number, number]; scale?: number }) => {
  const groupRef = useRef<THREE.Group>(null);

  const hexShape = useMemo(() => {
    const shape = new THREE.Shape();
    const sides = 6;
    const radius = 0.5;
    for (let i = 0; i <= sides; i++) {
      const angle = (i / sides) * Math.PI * 2 - Math.PI / 2;
      const x = Math.cos(angle) * radius;
      const y = Math.sin(angle) * radius;
      if (i === 0) shape.moveTo(x, y);
      else shape.lineTo(x, y);
    }
    return shape;
  }, []);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.3;
      groupRef.current.rotation.z = state.clock.elapsedTime * 0.2;
    }
  });

  return (
    <Float speed={2.2} rotationIntensity={0.6} floatIntensity={0.6}>
      <group ref={groupRef} position={position} scale={scale}>
        <mesh>
          <shapeGeometry args={[hexShape]} />
          <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.4} side={THREE.DoubleSide} />
        </mesh>
        
        {/* Inner hex */}
        <mesh scale={0.6}>
          <shapeGeometry args={[hexShape]} />
          <meshBasicMaterial color="#00ffff" wireframe transparent opacity={0.6} side={THREE.DoubleSide} />
        </mesh>
        
        {/* Center dot */}
        <mesh>
          <circleGeometry args={[0.08, 6]} />
          <meshBasicMaterial color="#ffffff" transparent opacity={0.8} />
        </mesh>
      </group>
    </Float>
  );
};

// DNA-like Helix Structure
const HelixStructure = ({ position, scale = 1 }: { position: [number, number, number]; scale?: number }) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.elapsedTime * 0.5;
    }
  });

  const helixPoints = useMemo(() => {
    const points: { pos1: [number, number, number]; pos2: [number, number, number] }[] = [];
    for (let i = 0; i < 20; i++) {
      const y = (i - 10) * 0.1;
      const angle = i * 0.5;
      points.push({
        pos1: [Math.cos(angle) * 0.3, y, Math.sin(angle) * 0.3],
        pos2: [Math.cos(angle + Math.PI) * 0.3, y, Math.sin(angle + Math.PI) * 0.3],
      });
    }
    return points;
  }, []);

  return (
    <Float speed={1.2} rotationIntensity={0.2} floatIntensity={0.5}>
      <group ref={groupRef} position={position} scale={scale}>
        {helixPoints.map((point, i) => (
          <group key={i}>
            <mesh position={point.pos1}>
              <sphereGeometry args={[0.03, 6, 6]} />
              <meshBasicMaterial color="#00d4ff" transparent opacity={0.8} />
            </mesh>
            <mesh position={point.pos2}>
              <sphereGeometry args={[0.03, 6, 6]} />
              <meshBasicMaterial color="#00ffff" transparent opacity={0.8} />
            </mesh>
            {i % 3 === 0 && (
              <mesh position={[0, point.pos1[1], 0]}>
                <cylinderGeometry args={[0.01, 0.01, 0.6, 4]} />
                <meshBasicMaterial color="#00d4ff" wireframe transparent opacity={0.4} />
              </mesh>
            )}
          </group>
        ))}
      </group>
    </Float>
  );
};

// Main Holographic Scene
const HolographicScene = () => {
  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} intensity={0.5} />
      
      {/* Helmet - top left area */}
      <HelmetModel position={[-4, 2, -2]} scale={1.2} />
      
      {/* Arc Reactor - right side */}
      <ArcReactor3D position={[4.5, 0, -1]} scale={1.5} />
      
      {/* Gauntlet - bottom left */}
      <GauntletModel position={[-4.5, -1.5, -1.5]} scale={1} />
      
      {/* Hex Panels - scattered */}
      <HexPanel position={[3.5, 2.5, -3]} scale={0.8} />
      <HexPanel position={[-3, -2.5, -2]} scale={0.6} />
      
      {/* Helix - right side lower */}
      <HelixStructure position={[5, -2, -2]} scale={1.2} />
    </>
  );
};

const HolographicModels = () => {
  return (
    <div className="absolute inset-0 pointer-events-none z-0">
      <Canvas
        camera={{ position: [0, 0, 8], fov: 50 }}
        style={{ background: "transparent" }}
        gl={{ alpha: true, antialias: true }}
      >
        <HolographicScene />
      </Canvas>
    </div>
  );
};

export default HolographicModels;